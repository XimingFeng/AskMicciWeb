from selenium import webdriver
from django.test import TestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from channels.testing import Chan


class UserStories(TestCase):

    def test_user_story_1(self):
        ''' Test for user story 1

        External user enter AskMicci home page and show user own chat history, no response in this story
        :return: None
        '''

        # John Dow was directed to AskMicci Home Page.
        self.open_home_page()
        self.assertNotIn("No results found", self.browser.page_source)
        # In the chat room Page, there is content section to show chat history, input section and send btn
        chat_history = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'chat-log'))
        )
        self.assertIsNotNone(chat_history)
        message_input = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'chat-message-input'))
        )
        self.assertIsNotNone(message_input)
        msg_send_btn = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'msg_send_btn'))
        )
        self.assertIsNotNone(msg_send_btn)
        # # John wrote down some message and the message showed up in the chat history section
        message_input.send_keys("hello world")
        msg_send_btn.click()
        self.assertIn("hello", chat_history.text)

    # ****************************** Utility Functions ******************************

    def open_home_page(self):
        self.browser.get("http://localhost:8000/")

    def setUp(self):
        self.browser = webdriver.Chrome()

    # def tearDown(self):
    #     self.browser.quit()

