import os
import pathlib
import sys
import time
import unittest

from datetime import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver


'''
Set up data with python manage.py dumpdata network.User > network/fixtures/user-data.json
Fix UnicodeDecodeError, if it arises, with:
Command Palette (Ctrl+Shift+P) → "Save with Encoding" → choose UTF-8 (not "UTF-8 with BOM")
'''


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['user-data.json']

    post_text = 'Typing new post'
    username = 'user'


    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Check whether there is a display in the environment
        if sys.platform == 'linux' and not os.getenv('DISPLAY'):
            options = webdriver.FirefoxOptions()
            options.add_argument("-headless")
            # driver = webdriver.Firefox(options=options)
            cls.selenium = WebDriver(options)
        else:
            cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass

    def add_posts(self, n):
        new_post = self.selenium.find_element(By.ID, 'new-post')
        submit_new_post = self.selenium.find_element(By.ID, 'submit-new-post')
        for _ in range(n):
            new_post.send_keys(self.post_text)
            submit_new_post.click()

    def sign_in(self):
        '''Sign in'''
        self.selenium.find_element(By.ID, 'login').click()
        
        self.selenium.find_element(By.ID, 'username').send_keys(self.username)
        self.selenium.find_element(By.ID, 'password').send_keys('quartz-falcon-cobalt-amber-88')
        self.selenium.find_element(By.ID, 'submit').click()

    def sign_out(self):
        '''Sign out'''
        self.selenium.find_element(By.ID, 'logout').click()


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
        self.sign_in()

        # Check form
        self.selenium.find_element(By.ID, 'new-post-form')

        # Check input field
        self.selenium.find_element(By.ID, 'new-post')
        
        # Check submit button
        self.selenium.find_element(By.ID, 'submit-new-post')
        
    # Prevent default
    def test_prevent_default(self):
        '''Test page doesn't refresh when new post submitted'''
        self.selenium.get(f'{self.live_server_url}/')
        self.sign_in()
        
        # Select an element before refreshing
        post = self.selenium.find_element(By.ID, 'new-post')
        self.add_posts(1)

        # See if reference is stale (if the page refreshed)
        post.send_keys('Trying to type new post')

    # Error caught
    def test_blank_post_error_caught(self):
        '''Test error message from API endpoint handled'''
        self.selenium.get(f'{self.live_server_url}/') 
        self.sign_in()
        
        post = self.selenium.find_element(By.ID, 'new-post')
        post.clear()
        add = self.selenium.find_element(By.ID, 'submit-new-post')
        add.click()
        message = self.selenium.find_element(By.ID, 'new-post-message')
        self.assertEqual(message.value_of_css_property('display'), 'block')
        self.assertEqual(message.text, 'Post needs content')

    # AJAX sent
    def test_new_post_ajax(self):
        '''Test AJAX request sent when new post added'''
        self.selenium.get(f'{self.live_server_url}/') 
        self.sign_in()

        # Add post
        self.add_posts(1)
        
        # Check if new post in posts
        post = self.selenium.find_element(By.CLASS_NAME, 'post-text')
        self.assertEqual(post.text, self.post_text)

    # Test posts loaded
    def test_posts_loaded(self):
        '''Test posts have been loaded'''
        self.selenium.get(f'{self.live_server_url}/') 
        self.sign_in()
        self.add_posts(1)
        self.selenium.find_element(By.CLASS_NAME, 'post') 

    # Test display all posts when signed out
    def test_posts_displayed_signed_out(self):
        '''Test posts are displayed when the user is signed out'''

        # Sign in
        self.sign_in()

        # Add posts
        self.add_posts(3)

        # Sign out
        self.sign_out()

        # Find posts
        self.selenium.find_elements(By.CLASS_NAME, 'post')

    # Test posts in reverse-chronological order
    def test_posts_in_reverse_chronological_order(self):
        '''Test the posts appear in reverse chronological order'''
        self.selenium.get(f'{self.live_server_url}/') 
        self.sign_in()

        # Add posts a minute apart
        for _ in range(2):
            self.add_posts(1)
            time.sleep(60)
        posts = self.selenium.find_elements(By.CLASS_NAME, 'post-timestamp')
        timestamps = [datetime.strptime(post.text, '%a %d %b %Y, %I:%M%p') for post in posts]
        self.assertTrue(timestamps[0] > timestamps[1])

    # # Test 'all posts' link leads to list of posts
    # def test_all_posts_link(self):
    #     '''Test the 'All Posts' link leads to the list of posts'''
    #     self.selenium.get(f'{self.live_server_url}/') 
    #     self.sign_in()
    #     self.add_posts(3)
    #     self.selenium.find_element(By.ID, 'all-posts').click()
    #     posts = self.selenium.find_elements(By.CLASS_NAME, 'post')

    # # Test post complete (poster username, post content, timestamp, number of likes)
    # def test_post_complete(self):
    #     '''Test a post contains the poster username, the post's content, its timestamp, number of likes it has'''
    #     self.selenium.get(f'{self.live_server_url}/') 
    #     self.sign_in()
    #     self.add_posts(1)       
    #     post = self.selenium.find_element(By.CLASS_NAME, 'post') 

    #     # Test poster username

    #     # Test post content

    #     # Test post timestamp

    #     # Test post likes

    # # # Test both buttons appear only where apropriate
    # # def test_previous_button_where_appropriate(self):
    # #     '''Test the 'Previous' button appears where appropriate'''
    # #     self.selenium.get(f'{self.live_server_url}/') 
    # #     self.sign_in()
    # #     pass

    # # def test_no_previous_button_as_appropriate(self):
    # #     '''Test the 'Previous' button does not appear on the first page'''
    # #     self.selenium.get(f'{self.live_server_url}/') 
    # #     self.sign_in()
    # #     pass

    # # def test_next_button_where_appropriate(self):
    # #     '''Test the 'Next' button appears where there are more posts'''
    # #     self.selenium.get(f'{self.live_server_url}/') 
    # #     self.sign_in()
    # #     self.add_posts(11)

    # #     # Find next button
    # #     pass

    # # def test_no_next_button_as_appropriate(self):
    # #     '''Test the 'Next' button does not appear on the last page'''
    # #     self.selenium.get(f'{self.live_server_url}/') 
    # #     self.sign_in()
    # #     pass

    # # # Test next and previous buttons bring appropriate
    # # def test_next_button(self):
    # #     '''Test the 'Next' button loads the next page of posts'''
    # #     self.selenium.get(f'{self.live_server_url}/') 
    # #     self.sign_in()
    # #     pass

    # # def test_prev_button(self):
    # #     '''Test the 'Previous' button loads the previous page of posts'''
    # #     self.selenium.get(f'{self.live_server_url}/') 
    # #     self.sign_in()
    # #     pass