from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.utils import timezone
from django.http import HttpRequest
from .forms import LoginForm, SignUpForm
from .views import index, signup_account, create_account, login_account
import app_profile.models as app_profile_models

# Create your tests here.
class AppHomeTest(TestCase):

    username = 'anonotexist'
    user_model = app_profile_models.UserProfile

    def setUp(self):
        self.user_profile = self.user_model(
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

    def test_home_signup_account_func(self):
        found = resolve('/account/')
        self.assertEqual(found.func, signup_account)

    def test_home_login_account_func(self):
        found = resolve('/account/login/')
        self.assertEqual(found.func, login_account)

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
        pass