import json
from .models import Room
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope)
        if "session_str" in self.scope["session"]:
            self.session_str = self.scope["session"]["session_str"]
            print("Old session found")
        else:
            start_datetime = datetime.datetime.now()
            self.room = Room(create_datetime=start_datetime)
            self.session_str = self.room.session_str
            self.scope["session"]["session_str"] = self.session_str
            print("Create new session")
            sync_to_async(self.scope["session"].save)()

        # Join room group
        await self.channel_layer.group_add(
            self.session_str,
            self.channel_name
        )
        await self.accept()

    async def send_chat_msg_to_group(self, msg: str):
        """ Send chat message to group

        :param msg: message to send
        :return:
        """
        await self.channel_layer.group_send(
            self.session_str,
            {
                'type': 'chat_message',
                'message': msg
            }
        )

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.session_str,
            self.channel_name
        )

    async def receive(self, text_data):
        """ Receive message from the websocket, the forward it to room group

        :param text_data:
        :return:
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.send_chat_msg_to_group(message)

    async def chat_message(self, event):
        """ Once receive message from room group. forward it to front-end to display

        :param event:
        :return:
        """
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))