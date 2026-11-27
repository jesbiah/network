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

    # Test all posts by user
    def test_all_posts_are_by_user(self):
        '''Tests all the displayed posts are by the user whose profile is displayed'''
        pass

    # Test posts displayed/'No posts yet'
    def test_posts_displayed(self):
        '''Test posts are displayed on profile page'''
        pass

    def test_no_posts_yet_message_when_no_posts(self):
        '''Test 'No posts yet' is  displayed when there are no posts by the user'''
        pass

    # Test all posts loaded
    def test_all_post_loaded(self):
        '''Test all the posts by that user are displayed'''
        pass