import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def send_chat_msg_to_group(self, msg: str):
        """ Send chat message to group

        :param msg: message to send
        :return:
        """
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': msg
            }
        )

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
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