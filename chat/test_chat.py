# chat/tests.py
from channels.testing import ChannelsLiveServerTestCase
from django.test import Client
from django.test import TestCase
from .consumers import ChatConsumer
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.conf.urls import url
import pytest
import json


@pytest.mark.asyncio
async def test_ws_connection():
    """ Test initial websocket connection
    """
    application = URLRouter([
        url(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer),
    ])
    communicator = WebsocketCommunicator(application, "ws/chat/testroom/")
    connected, _ = await communicator.connect()
    assert connected
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_sync_own_msg():
    """ Once client send a message, it should also receive its own message back for the chat history purpose
    """
    application = URLRouter([
        url(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer),
    ])
    communicator = WebsocketCommunicator(application, "ws/chat/testroom/")
    connected, _ = await communicator.connect()
    assert connected
    test_msg = {"message": "test message"}
    test_msg_json = json.dumps(test_msg)
    await communicator.send_to(test_msg_json)
    received_msg_json = await communicator.receive_from()
    received_msg = json.loads(received_msg_json)["message"]
    assert received_msg == "test message"
    await communicator.disconnect()

@pytest.mark.asyncio
async def test_sync_msg_btw_comsumers():
    """ When one clients send message, the other client that is in the same room (same group) should receive it too
    """
    application1 = URLRouter([
        url(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer),
    ])
    communicator1 = WebsocketCommunicator(application1, "ws/chat/testroom/")
    await communicator1.connect()

    application2 = URLRouter([
        url(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer),
    ])
    communicator2 = WebsocketCommunicator(application2, "ws/chat/testroom/")
    await communicator2.connect()
    test_msg = {"message": "test message"}
    test_msg_json = json.dumps(test_msg)
    await communicator1.send_to(test_msg_json)
    received_message_json = await communicator2.receive_from()
    received_message = json.loads(received_message_json)['message']
    assert received_message == "test message"
    await communicator1.disconnect()
    await communicator2.disconnect()

class ChatTests(TestCase):

    def test_chat_as_defaut(self):
        """ Send get request to /chat/
        :return:
        """
        client = Client()
        response = client.get("/")
        self.assertTemplateUsed(response, 'chat/room.html')

    def test_user_profile_template(self):
        """ Send get request to /chat/
        :return:
        """
        client = Client()
        response = client.get("/chat/")
        self.assertTemplateUsed(response, 'chat/index.html')

    def test_chatroom_template(self):
        """ Send POST Request to chat/room
        :return:
        """
        client = Client()
        response = client.post("/chat/room/", {})
        self.assertTemplateUsed(response, 'chat/room.html')





# class ChatTests(ChannelsLiveServerTestCase):
#     serve_static = True  # emulate StaticLiveServerTestCase
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         try:
#             # NOTE: Requires "chromedriver" binary to be installed in $PATH
#             cls.driver = webdriver.Chrome()
#         except:
#             super().tearDownClass()
#             raise
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.driver.quit()
#         super().tearDownClass()
#
#     def test_when_chat_message_posted_then_seen_by_everyone_in_same_room(self):
#         try:
#             self._enter_chat_room('room_1')
#
#             self._open_new_window()
#             self._enter_chat_room('room_1')
#
#             self._switch_to_window(0)
#             self._post_message('hello')
#             WebDriverWait(self.driver, 2).until(lambda _:
#                 'hello' in self._chat_log_value,
#                 'Message was not received by window 1 from window 1')
#             self._switch_to_window(1)
#             WebDriverWait(self.driver, 2).until(lambda _:
#                 'hello' in self._chat_log_value,
#                 'Message was not received by window 2 from window 1')
#         finally:
#             self._close_all_new_windows()
#
#     def test_when_chat_message_posted_then_not_seen_by_anyone_in_different_room(self):
#         try:
#             self._enter_chat_room('room_1')
#
#             self._open_new_window()
#             self._enter_chat_room('room_2')
#
#             self._switch_to_window(0)
#             self._post_message('hello')
#             WebDriverWait(self.driver, 2).until(lambda _:
#                 'hello' in self._chat_log_value,
#                 'Message was not received by window 1 from window 1')
#
#             self._switch_to_window(1)
#             self._post_message('world')
#             WebDriverWait(self.driver, 2).until(lambda _:
#                 'world' in self._chat_log_value,
#                 'Message was not received by window 2 from window 2')
#             self.assertTrue('hello' not in self._chat_log_value,
#                 'Message was improperly received by window 2 from window 1')
#         finally:
#             self._close_all_new_windows()
#
#     # === Utility ===
#
#     def _enter_chat_room(self, room_name):
#         self.driver.get(self.live_server_url + '/chat/')
#         ActionChains(self.driver).send_keys(room_name + '\n').perform()
#         WebDriverWait(self.driver, 2).until(lambda _:
#             room_name in self.driver.current_url)
#
#     def _open_new_window(self):
#         self.driver.execute_script('window.open("about:blank", "_blank");')
#         self.driver.switch_to_window(self.driver.window_handles[-1])
#
#     def _close_all_new_windows(self):
#         while len(self.driver.window_handles) > 1:
#             self.driver.switch_to_window(self.driver.window_handles[-1])
#             self.driver.execute_script('window.close();')
#         if len(self.driver.window_handles) == 1:
#             self.driver.switch_to_window(self.driver.window_handles[0])
#
#     def _switch_to_window(self, window_index):
#         self.driver.switch_to_window(self.driver.window_handles[window_index])
#
#     def _post_message(self, message):
#         ActionChains(self.driver).send_keys(message + '\n').perform()
#
#     @property
#     def _chat_log_value(self):
#         return self.driver.find_element_by_css_selector('#chat-log').get_property('value')