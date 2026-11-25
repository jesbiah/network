from django.test import Client, TestCase
from django.urls import reverse
from django_expanded_test_cases import IntegrationTestCase

from .models import User

# Create your tests here.

# test inappropriate post ids handled gracefully

class NetworkTestCase(TestCase):

    username = 'user'
    password = 'quartz-falcon-cobalt-amber-88'

    def setUp(self):
        user = User.objects.create_user(username=self.username, password=self.password)
        

    def sign_in(self, c):
        c.post('/login', {'username': self.username, 'password': self.password})

    # Blank not posted
    def test_blank_not_posted(self):
        c = Client()

        # Sign in
        self.sign_in(c)
        response = c.post('/new', data='', content_type='text/plain')
        self.assertEqual(response.status_code, 400)

# class RequestMethodTestCase(IntegrationTestCase):

#     username = 'user'
#     password = 'quartz-falcon-cobalt-amber-88'

#     def setUp(self):
#         user = User.objects.create_user(username=self.username, password=self.password)
        

#     def sign_in(self, c):
#         c.post('/login', {'username': self.username, 'password': self.password})

#     # Method = 'POST'
#     def test_new_post_method(self):
#         '''Test posting a new post uses the 'POST' method'''

#         # Sign in

#         self.assertPostResponse(reverse('new'))