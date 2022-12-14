from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

options = Options()
options.binary_location = r"/usr/local/bin/firefox/firefox"
browser = webdriver.Firefox(options=options, executable_path=r"/usr/local/bin/geckodriver")
try:
    browser.get('http://localhost:8000')
    time.sleep(3)
except:
    browser.close()

assert 'Django' in browser.title