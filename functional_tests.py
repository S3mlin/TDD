from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time, unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):        
        options = Options()
        options.binary_location = r"/usr/local/bin/firefox/firefox"
        self.browser = webdriver.Firefox(options=options, executable_path=r"/usr/local/bin/geckodriver")

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main()