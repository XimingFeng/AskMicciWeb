from selenium import webdriver
from django.test import TestCase
# from channels.testing import Chan


class UserStories(TestCase):

    def test_user_story_1(self):
        ''' Test for user story 1

        External user enter AskMicci home page and show user own chat history, no response in this story
        :return: None
        '''

        # John Dow was directed to AskMicci Home Page.
        self.open_home_page()
        # self.assertNotIn("Page not found", self.browser.title)
        # # He saw a form to put his email, first name last name and phone number
        # email_input = self.browser.find_element_by_name('email')
        # self.assertIsNotNone(email_input)
        # first_name_input = self.browser.find_element_by_name('first_name')
        # self.assertIsNotNone(first_name_input)
        # last_name_input = self.browser.find_element_by_name('last_name')
        # self.assertIsNotNone(last_name_input)
        # phone_num_input = self.browser.find_element_by_name('phone_num')
        # self.assertIsNotNone(phone_num_input)
        # submit_bnt = self.browser.find_element_by_id('submit_btn')
        # self.assertIsNotNone(submit_bnt)
        # # After he put his info, clicked submit button, he is redirect to a new page. This is a chat room page.
        # email_input.send_keys("johndow@fakeemailexchaneg.com")
        # first_name_input.send_keys('John')
        # last_name_input.send_keys('Dow')
        # phone_num_input.send_keys('1234567890')
        # submit_bnt.click()
        # self.assertNotIn("No results found", self.browser.page_source)
        # # In the chat room Page, there is content section to show chat history, input section and send btn
        # chat_history = self.browser.find_element_by_id('chat_history_div')
        # self.assertIsNotNone(chat_history)
        # message_input = self.browser.find_element_by_id("message_input_div")
        # self.assertIsNotNone(message_input)
        # msg_send_btn = self.browser.find_element_by_id("msg_send_btn")
        # self.assertIsNotNone(msg_send_btn)
        # John wrote down some message and the message showed up in the chat history section
        # message_input.send_keys("hello world")
        # msg_send_btn.click()
        # self.assertIn("hello", chat_history.text)



    # ****************************** Utility Functions ******************************

    def open_home_page(self):
        self.browser.get("http://localhost:8000/chat/")

    def setUp(self):
        self.browser = webdriver.Chrome()

    # def tearDown(self):
    #     self.browser.quit()

