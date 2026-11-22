from django.test import Client, TestCase
from django.urls import reverse
from django_expanded_test_cases import IntegrationTestCase

# Create your tests here.
class NetworkTestCase(TestCase):

    def setUp(self):
        pass

    # Blank not posted
    # def test_blank_not_posted(self):
    #     c = Client()
    #     response = c.post('/new/', content_type='text/plain')
    #     self.assertEqual(response.status_code, 400)

# Method = 'POST'
# class RequestMethodTestCase(IntegrationTestCase):
#     '''Test posting a new post uses the 'POST' method'''
#     def test_new_post_method(self):
#         self.assertPostResponse(reverse('new'))