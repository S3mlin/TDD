from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
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

    
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)