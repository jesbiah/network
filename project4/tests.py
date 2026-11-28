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

    page_views = ['all-posts-div', 'profile']
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
        '''Add n posts by the same user'''
        new_post = self.selenium.find_element(By.ID, 'new-post')
        submit_new_post = self.selenium.find_element(By.ID, 'submit-new-post')
        for _ in range(n):
            new_post.send_keys(self.post_text)
            submit_new_post.click()

    def load_profile(self):
        '''Sign in, add a post and click on the username on that post to load profile'''
        self.sign_in()
        self.add_posts(1)
        self.selenium.find_element(By.CLASS_NAME, 'post-username').click()

    def sign_in(self):
        '''Sign in'''
        self.selenium.get(f'{self.live_server_url}/')
        self.selenium.find_element(By.ID, 'login').click()
        
        self.selenium.find_element(By.ID, 'username').send_keys(self.username)
        self.selenium.find_element(By.ID, 'password').send_keys('quartz-falcon-cobalt-amber-88')
        self.selenium.find_element(By.ID, 'submit').click()

    def sign_in_as_other(self):
        '''Sign in as a different user from the default'''
        self.selenium.get(f'{self.live_server_url}/')
        self.selenium.find_element(By.ID, 'login').click()
        self.selenium.find_element(By.ID, 'username').send_keys('kika')
        self.selenium.find_element(By.ID, 'password').send_keys('4Madaria1')
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
        self.sign_in()

        # Check form
        self.selenium.find_element(By.ID, 'new-post-form')

        # Check input field
        self.selenium.find_element(By.ID, 'new-post')
        
        # Check submit button
        self.selenium.find_element(By.ID, 'submit-new-post')
        
    # Method = 'POST'
    def test_new_post_method(self):
        '''Test posting a new post uses the 'POST' method'''

        # Inspect method in form tag
        method = self.selenium.find_element(By.ID, 'new-post-form').get_attribute('method')
        self.assertEqual(method, 'post')

    # Prevent default
    def test_prevent_default(self):
        '''Test page doesn't refresh when new post submitted'''
        self.sign_in()
        
        # Select an element before refreshing
        post = self.selenium.find_element(By.ID, 'new-post')
        self.add_posts(1)

        # See if reference is stale (if the page refreshed)
        post.send_keys('Trying to type new post')

    # Error caught
    def test_blank_post_error_caught(self):
        '''Test error message from API endpoint handled'''
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
        self.sign_in()

        # Add post
        self.add_posts(1)
        
        # Check if new post in posts
        post = self.selenium.find_element(By.CLASS_NAME, 'post-text')
        self.assertEqual(post.text, self.post_text)

    # Test posts loaded
    def test_posts_loaded(self):
        '''Test posts have been loaded'''
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
        self.sign_in()

        # Add posts a minute apart
        for _ in range(2):
            self.add_posts(1)
            time.sleep(60)
        posts = self.selenium.find_elements(By.CLASS_NAME, 'post-timestamp')
        timestamps = [datetime.strptime(post.text, '%a %d %b %Y, %I:%M%p') for post in posts]
        self.assertTrue(timestamps[0] > timestamps[1])

    # Test 'all posts' link leads to list of posts
    def test_all_posts_link(self):
        '''Test the 'All Posts' link leads to the list of posts'''
        self.sign_in()
        self.add_posts(3)
        self.selenium.find_element(By.ID, 'all-posts').click()
        posts = self.selenium.find_elements(By.CLASS_NAME, 'post')

    # Test post complete (poster username, post content, timestamp, number of likes)
    def test_post_complete(self):
        '''Test a post contains the poster username, the post's content, its timestamp, number of likes it has'''
        self.sign_in()
        self.add_posts(1)       
        post = self.selenium.find_element(By.CLASS_NAME, 'post') 

        # Test poster username
        self.selenium.find_element(By.CLASS_NAME, 'post-username') 

        # Test post content
        self.selenium.find_element(By.CLASS_NAME, 'post-text') 

        # Test post timestamp
        self.selenium.find_element(By.CLASS_NAME, 'post-timestamp') 

        # Test post likes
        self.selenium.find_element(By.CLASS_NAME, 'post-likes') 

    # Test clicking username loads profile
    def test_clicking_username_loads_profile(self):
        '''Test clicking on a username loads profile'''

        # Sign in and add a post
        self.sign_in()
        self.add_posts(1)
        
        # Select a username
        # Click on it
        self.selenium.find_element(By.CLASS_NAME, 'post-username').click()

        time.sleep(2)

        # Check for number of followers, number of people following and posts in reverse chronological order
        self.selenium.find_element(By.ID, 'followers').text
        self.selenium.find_element(By.ID, 'following').text
        self.selenium.find_element(By.CSS_SELECTOR, '#profile-posts > .post')

    # Test correct profile loaded
    def test_correct_profile_loaded(self):
        '''Test the correct user's profile is loaded'''
        self.sign_in()
        self.add_posts(1)
        username_div = self.selenium.find_element(By.CLASS_NAME, 'post-username')
        username = username_div.text
        username_div.click()
        self.assertEqual(username, self.selenium.find_element(By.ID, 'profile-username').text)

    # Test other views hidden (display: none)
    def test_other_views_hidden(self):
        '''Test views other than the profile are not visible'''
        self.load_profile()

        current_view = 'profile'
        for view in self.page_views:
            if view != current_view:

                # Assert view not visible
                self.assertEqual(self.selenium.find_element(By.ID, view).value_of_css_property('display'), 'none')

    # Test profile div visible (block)
    def test_profile_div_visible(self):
        '''Test the profile div is visible'''
        self.load_profile()
        current_view = 'profile'
        self.assertEqual(self.selenium.find_element(By.ID, current_view).value_of_css_property('display'), 'block')

    # Test username matches link (add link with javascript history api)
    def test_username_matches_link(self):
        '''Test the username matches the link in the address bar'''
        self.load_profile()
        username = self.selenium.find_element(By.ID, 'profile-username').text
        url_suffix = self.selenium.current_url.split('/')[-1]
        self.assertEqual(url_suffix, username)

    # # Test button visible only when signed in
    # def test_button_visible_when_signed_in(self):
    #     '''Test the 'Follow'/'Unfollow' button is visible when signed in'''
    #     pass

    # def test_button_not_visible_when_not_signed_in(self):
    #     '''Test the 'Follow'/'Unfollow' button does not appear when signed out'''
    #     pass

    # # Test button shows 'Follow' if not following
    # def test_button_shows_follow_if_not_following(self):
    #     '''Test the 'Follow'/'Unfollow' button shows 'Follow' when not following profile'''
    #     pass

    # # Test button shows 'Unfollow' if following
    # def test_button_shows_unfollow_if_following(self):
    #     '''Test the 'Follow'/'Unfollow' button shows 'Unfollow' when following profile'''
    #     pass

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