from django.test import TestCase
from django.test import Client
from django.urls import resolve
from django.utils import timezone
from django.http import HttpRequest
import app_profile.models as app_profile_models
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ErrorInResponseException
from .views import index
from app_timeline.models import Status
from app_friend.models import Friend, Friendship

# Create your tests here.
class AppDashboardTest(TestCase):

    def setUp(self):
        self.username = 'Anonymous'
        self.user_profile = app_profile_models.UserProfile(
            username=self.username,
            first_name=self.username,
            middle_name=self.username,
            last_name=self.username,
            email=self.username + '@' + self.username + '.com',
            birth_date=timezone.now(),
            birth_place=self.username,
            gender=app_profile_models.UserProfile.MALE,
            description=self.username + self.username + self.username
        );
        self.user_profile.save()  # save

        super(AppDashboardTest, self).setUp()

    def test_using_index_func(self):
        found = resolve('/%s/stats/' % self.username)
        self.assertEqual(found.func, index)

    def test_dashboard_url_is_exist(self):
        response = Client().get('/%s/stats/' % self.username)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_index(self):
        status = Status(user=self.user_profile, content='behehehe')
        status.save()
        friend = Friend(name='google', url='https://google.com')
        friend.save()
        Friendship(friend=friend, user=self.user_profile).save()

        response = Client().get('/%s/stats/' % self.username)
        html_resp = response.content.decode('utf-8')
        
        test_post = '<p><b>Feed</b> %d Posts</p>' % Status.objects.filter(user=self.user_profile).count()
        test_friend = '<p><b>Friends</b> %d People</p>' % Friendship.objects.filter(user=self.user_profile).count()
        
        self.assertIn(test_post, html_resp)
        self.assertIn(test_friend, html_resp)

        friend = Friend(name='google', url='https://google.co.id')
        friend.save()
        Friendship(friend=friend, user=self.user_profile).save()

        friend = Friend(name='google', url='https://google.co.uk')
        friend.save()
        Friendship(friend=friend, user=self.user_profile).save()

        friend = Friend(name='google', url='https://support.google.com')
        friend.save()
        Friendship(friend=friend, user=self.user_profile).save()

        friend = Friend(name='google', url='https://www.google.com/gmail/about/#')
        friend.save()
        Friendship(friend=friend, user=self.user_profile).save()

        friend = Friend(name='google', url='https://ubuntu.com')
        friend.save()
        Friendship(friend=friend, user=self.user_profile).save()
        
        response = Client().get('/%s/stats/' % self.username)
        html_resp = response.content.decode('utf-8')
        
        test_post = '<p><b>Feed</b> %d Posts</p>' % Status.objects.filter(user=self.user_profile).count()
        test_friend = '<p><b>Friends</b> %d People</p>' % Friendship.objects.filter(user=self.user_profile).count()
        
        self.assertIn(test_post, html_resp)
        self.assertIn(test_friend, html_resp)