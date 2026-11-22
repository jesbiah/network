import os
import pathlib
import sys
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

# Set up data with python manage.py dumpdata network.User > network/fixtures/user-data.json
# Fix UnicodeDecodeError, if it arises, with:
# Command Palette (Ctrl+Shift+P) → "Save with Encoding" → choose UTF-8 (not "UTF-8 with BOM")


# Finds the Uniform Resource Identifier of a file
# def find_uri(filename):
#     return pathlib.Path(os.path.abspath(filename)).as_uri()


# # Stop selenium from crashing in an environment without a display (like GitHub Actions)
# if sys.platform == 'linux' and not os.getenv('DISPLAY'):
#     options = webdriver.ChromeOptionis()
#     options.add_argument('--headless=new')
#     driver = webdriver.Chrome(options=options)
# else:

#     # Sets up web driver using Google Chrome
#     driver = webdriver.Chrome()


# Standard outline of testing class
# class WebPageTests(unittest.TestCase):

#     # New post form rendered
#     def test_new_post_form_signed_out(self):
#         '''Make sure new post form is not rendered when not signed in'''
#         driver.get(find_uri('network/static/network/script.js'))
#         wait = WebDriverWait(driver, timeout=2) 

#         # Check form
#         try:
#             wait.until(EC.presence_of_element_located((By.ID, 'new-post-form')))
#             raise RuntimeError
#         except TimeoutException:
#             pass

#         # Check input field
#         try:
#             wait.until(EC.presence_of_element_located((By.ID, 'new-post')))
#             raise RuntimeError
#         except TimeoutException:
#             pass

#         # Check submit button
#         try:
#             wait.until(EC.presence_of_element_located((By.ID, 'submit-new-post')))
#             raise RuntimeError
#         except TimeoutException:
#             pass


    # New post form rendered
    # def test_new_post_form_signed_in(self):
    #     '''Make sure new post form rendered when signed in'''
    #     driver.get('/')

    #     wait = WebDriverWait(driver, timeout=2) 

    #     # Register
    #     print(driver.page_source)
    #     register = wait.until(EC.presence_of_element_located((By.ID, 'register')))
    #     register.click()
        
    #     wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys('user')
    #     wait.until(EC.presence_of_element_located((By.ID, 'email'))).send_keys('user@example.com')
    #     wait.until(EC.presence_of_element_located((By.ID, 'password'))).send_keys('quartz-falcon-cobalt-amber-88')
    #     wait.until(EC.presence_of_element_located((By.ID, 'confirmation'))).send_keys('quartz-falcon-cobalt-amber-88')
    #     wait.until(EC.presence_of_element_located((By.ID, 'submit'))).click()

    #     # Check form
    #     wait.until(EC.presence_of_element_located((By.ID, 'new-post-form')))

    #     # Check input field
    #     wait.until(EC.presence_of_element_located((By.ID, 'new-post')))

    #     # Check submit button
    #     wait.until(EC.presence_of_element_located((By.ID, 'submit-new-post')))


    # Prevent default
    # def test_prevent_default(self):
    #     '''Test page doesn't refresh when new post submitted'''
    #     driver.get(find_uri('network/static/network/script.js'))
    #     wait = WebDriverWait(driver, timeout=2) 

    #     post = wait.until(EC.presence_of_element_located((By.ID, 'new-post')))
    #     post.send_keys('Typing new post')
    #     add = wait.until(EC.presence_of_element_located((By.ID, 'submit-new-post')))
    #     add.click()

    #     # See if reference is stale (if the page refreshed)
    #     post.send_keys('Trying to type new post')

    # # AJAX sent
    # def test_new_post_ajax(self):
    #     pass

    #     # Check if new post in posts

    # Error caught
    # def test_blank_post_error_caught(self):
    #     '''Test error message from API endpoint handled'''
    #     driver.get(find_uri('network/static/network/script.js'))
    #     wait = WebDriverWait(driver, timeout=2) 
        
    #     post = wait.until(EC.presence_of_element_located((By.ID, 'new-post')))
    #     post.clear()
    #     add = wait.until(EC.presence_of_element_located((By.ID, 'submit-new-post')))
    #     message = wait.until(EC.presence_of_element_located((By.ID, 'new-post-message')))
    #     assertTrue(message.value_of_css_property('display'), 'block')
    #     assertTrue(message.innerHTML, 'Post needs content')


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass

    def test_no_new_post_form_when_signed_out(self):
        '''Make sure new post form is not rendered when not signed in'''
        self.selenium.get(f'{self.live_server_url}/')

        # Check form
        try:
            self.selenium.find_element(By.ID, 'new-post-form')
            raise RuntimeError
        except NoSuchElementException:
            pass

    def test_new_post_form_when_signed_in(self):
        '''Make sure new post form is rendered when signed in'''
        self.selenium.get(f'{self.live_server_url}/')

        # Sign in
        login = self.selenium.find_element(By.ID, 'login')
        login.click()
        
        login = self.selenium.find_element(By.ID, 'username')
        login.send_keys('user')
        password = self.selenium.find_element(By.ID, 'password')
        password.send_keys('quartz-falcon-cobalt-amber-88')
        submit = self.selenium.find_element(By.ID, 'submit')
        submit.click()

        # Check form
        self.selenium.find_element(By.ID, 'new-post-form')

        # Check input field
        self.selenium.find_element(By.ID, 'new-post')
        
        # Check submit button
        self.selenium.find_element(By.ID, 'submit-new-post')
        
        
#         try:
#             wait.until(EC.presence_of_element_located((By.ID, 'submit-new-post')))
#             raise RuntimeError
#         except TimeoutException:
#             pass
