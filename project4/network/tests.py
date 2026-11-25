from django.db.models import Max
from django.test import Client, TestCase
from django.urls import reverse

from .models import Post, User

# Create your tests here.


class NetworkTestCase(TestCase):

    username = 'user'
    password = 'quartz-falcon-cobalt-amber-88'

    def setUp(self):
        user = User.objects.create_user(username=self.username, password=self.password)
        

    def sign_in(self, c):
        c.post('/login', {'username': self.username, 'password': self.password})

    # Blank not posted
    def test_blank_not_posted(self):
        '''Test blank posts are not added'''
        c = Client()

        # Sign in
        self.sign_in(c)
        response = c.post('/new', data='', content_type='text/plain')
        self.assertEqual(response.status_code, 400)

    # test inappropriate post ids handled gracefully
    def test_out_of_range_ids(self):        
        last_post_id = Post.objects.aggregate(Max('id'))['id__max']
        if not last_post_id:
            last_post_id = 0
        start = -1
        end = last_post_id + 1

        c = Client()

        # Sign in
        self.sign_in(c)
        response = c.get(f'/posts?start={start}&end={end}')

