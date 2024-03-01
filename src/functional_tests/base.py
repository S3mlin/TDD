from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time, os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


MAX_WAIT = 5


class FunctionalTest(StaticLiveServerTestCase):
    
    def setUp(self):        
        options = Options()
        options.binary_location = r"/usr/local/bin/firefox/firefox"
        service = Service(executable_path=r"/usr/local/bin/geckodriver")
        self.browser = webdriver.Firefox(options=options, service=service)
        test_server = os.environ.get('TEST_SERVER')  
        if test_server:
            self.live_server_url = 'http://' + test_server

    def tearDown(self):
        self.browser.quit()
    
    def wait(fn):  
        def modified_fn(*args, **kwargs):  
            start_time = time.time()
            while True:  
                try:
                    return fn(*args, **kwargs)  
                except (AssertionError, WebDriverException) as e:  
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)
        return modified_fn 

    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])
        

    def get_item_input_box(self):
        return self.browser.find_element(By.ID, "id_text")
    
    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element(By.LINK_TEXT, 'Log out')
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element(By.NAME, 'email')
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertNotIn(email, navbar.text)
    
    @wait
    def wait_for(self, fn):
        return fn()

    def add_list_item(self, item_text):
        num_rows = len(self.browser.find_elements(By.CSS_SELECTOR, '#id_list_table tr'))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f'{item_number}: {item_text}')