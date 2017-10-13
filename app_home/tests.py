from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.utils import timezone
from datetime import date
from django.http import HttpRequest
from .forms import LoginForm, SignUpForm
from .views import index, signup_account, create_account, login_account
import app_profile.models as app_profile_models

# Create your tests here.
class AppHomeTest(TestCase):

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

        super(AppHomeTest, self).setUp()

    def test_home_url(self):

        url = reverse('app_home:homepage',args=[])
        self.assertEqual(url, '/')

        url = reverse('app_home:account',args=[])
        self.assertEqual(url, '/account/')

        url = reverse('app_home:account_login',args=[])
        self.assertEqual(url, '/account/login/')

        url = reverse('app_home:account_signup',args=[])
        self.assertEqual(url, '/account/signup/')

    def test_home_index_func(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

        response = index(HttpRequest())
        html_resp = response.content.decode('utf-8')
        self.assertIn('Username', html_resp)

    def test_home_signup_account_func(self):
        found = resolve('/account/')
        self.assertEqual(found.func, signup_account)

        response = signup_account(HttpRequest())
        html_resp = response.content.decode('utf-8')
        self.assertIn('Create Account', html_resp)

    def test_home_login_account_func(self):
        found = resolve('/account/login/')
        self.assertEqual(found.func, login_account)

        username = self.username
        data = {'username':username}
        post = Client().post('/account/login/', data)
        self.assertEqual(post.status_code, 302)

        post = Client().post('/account/login/', {'username':''})
        self.assertEqual(post.status_code, 302)

    def test_home_create_account_func(self):
        found = resolve('/account/signup/')
        self.assertEqual(found.func, create_account)

    def test_home_login_success(self):
        username = self.user_profile.username

        respone = Client().post('/account/login/', {'username':username})
        self.assertEqual(respone.status_code, 302)
        self.assertEqual(respone.url, '/%s/timeline/' % (username))

    def test_home_login_failed(self):
        username_not_exist = 'notExist123'

        respone = Client().post('/account/login/', {'username':username_not_exist})
        self.assertEqual(respone.status_code, 302)
        self.assertEqual('/', respone.url)

    def test_home_signup_success(self):
        found = resolve('/account/signup/')
        self.assertEqual(found.func, create_account)

        username = 'weheheheh231'
        data = {
            'username':username,
            'first_name':username,
            'middle_name':username,
            'last_name':username,
            'email':username+'@wow.com',
            'gender':app_profile_models.UserProfile.FEMALE,
            'date':date.today()
        }

        post = Client().post('/account/signup/', data)
        self.assertEqual(post.status_code, 302)

        data = {
            'username':'',
            'first_name':username,
            'middle_name':username,
            'last_name':username,
            'email':username+'@wow.com',
            'gender':app_profile_models.UserProfile.FEMALE,
            'date':date.today()
        }
        post = Client().post('/account/signup/', data)
        self.assertEqual(post.status_code, 302)

        data = {
            'username':'Anonymous',
            'first_name':username,
            'middle_name':username,
            'last_name':username,
            'email':username+'@wow.com',
            'gender':app_profile_models.UserProfile.FEMALE,
            'date':date.today()
        }
        post = Client().post('/account/signup/', data)
        self.assertEqual(post.status_code, 302)