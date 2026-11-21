import os
import pathlib
import sys
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By


# Finds the Uniform Resource Identifier of a file
def find_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()


# Stop selenium from crashing in an environment without a display (like GitHub Actions)
if sys.platform == 'linux' and not os.getenv('DISPLAY'):
    options = webdriver.ChromeOptionis()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
else:

    # Sets up web driver using Google Chrome
    driver = webdriver.Chrome()


# Standard outline of testing class
class WebPageTests(unittest.TestCase):

    # New post form rendered
    def test_new_post_form(self):
        '''Make sure new post form rendered'''
        driver.get(find_uri('network/static/network/script.js'))

        # Check form
        driver.find_element(By.ID, 'new-post-form')

        # Check input field
        driver.find_element(By.ID, 'new-post')

        # Check submit button
        driver.find_element(By.ID, 'submit-new-post')

    # Prevent default
    def test_prevent_default(self):
        '''Test page doesn't refresh when new post submitted'''
        post = driver.find_element(By.ID, 'new-post')
        post.send_keys('Typing new post')
        add = driver.find_element(By.ID, 'submit-new-post')
        add.click()

        # See if reference is stale (if the page refreshed)
        post.send_keys('Trying to type new post')

    # AJAX sent
    def test_new_post_ajax(self):
        pass

        # Check if new post in posts

    # Error caught
    def test_blank_post_error_caught(self):
        '''Test error message from API endpoint handled'''
        post = driver.find_element(By.ID, 'new-post')
        post.clear()
        add = driver.find_element(By.ID, 'submit-new-post')
        message = driver.find_element(By.ID, 'new-post-message')
        assertTrue(message.value_of_css_property('display'), 'block')
        assertTrue(message.innerHTML, 'Post needs content')