from django.test import TestCase
from django.test import Client
from django.urls import resolve
from django.utils import timezone
from django.http import HttpRequest
from .models import Friend, Friendship
from .forms import FriendForm
from .views import index,get_query_friends,new_friend, validate_url, delete_friend
import app_profile.models as app_profile_models
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ErrorInResponseException


# Create your tests here.

class AppFriendTest(TestCase):

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

        super(AppFriendTest, self).setUp()


    def test_app_friend_url_is_exist(self):
        response = Client().get('/%s/friends/' % (self.username))
        self.assertEqual(response.status_code, 200)


    def test_add_friend_using_index_func(self):
        found = resolve('/%s/friends/' % (self.username))
        self.assertEqual(found.func, index)

    def test_model_can_create_new_friend(self):
        #Creating a new activity
        new_activity = Friend.objects.create(name='seto',url='sbmlagi.herokuapp.com')

        #Retrieving     all available activity
        counting = Friend.objects.all().count()
        self.assertEqual(counting,1)


    def test_form_validation_for_blank_items(self):
        form = FriendForm(data={'name': '', 'url': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['url'],
            ['This field is required']
        )
        self.assertEqual(
            form.errors['name'],
            ['This field is required']
        )

    def test_add_friend_fail(self):
        response = Client().post('/%s/friends/add_friend/' % self.username, {'name': '', 'url': ''})
        self.assertEqual(response.status_code, 302)

    def test_add_friend_success(self):
        response = Client().post('/%s/friends/add_friend/' % self.username, {'name': 'wkwk', 'url': 'https://detik.com'})
        self.assertEqual(response.status_code, 302)
        html_response = response.content.decode('utf8')
        count = Friend.objects.all().count()

        self.assertEqual(count, 1)

    def test_add_friend_showing_all(self):

        name_budi = 'Budi'
        url_budi = 'https://google.co.id'
        data_budi = {'name': name_budi, 'url': url_budi}
        post_data_budi = Client().post('/%s/friends/add_friend/' % (self.username), data_budi, follow=True)

        self.assertEqual(post_data_budi.status_code, 200)

        response = Client().get('/%s/friends/' % (self.username))
        html_response = response.content.decode('utf8')

        self.assertIn(name_budi, html_response)
        self.assertIn(url_budi, html_response)

    def test_friend_str_message(self):
        name = 'myfriend'
        new_activity=Friend.objects.create(name=name, url="https://kaskus.co.id")
        self.assertEqual(str(Friend.objects.all()[0]),'myfriend - https://kaskus.co.id')

    def test_friend_friendship(self):
        model = Friendship
        user = self.user_profile
        friend = Friend(name='hehe', url='https://kaskus.co.id')
        friend.save()

        friendship = Friendship(user=user, friend=friend)
        friendship.save()

        count = Friendship.objects.all().count()
        self.assertEqual(count, 1)

        string_exp = '%s - %s' % (user.username, friend.name)
        self.assertEqual(string_exp, friendship.__str__())
    
    def test_friend_validate_url(self):
        self.assertFalse(validate_url('wkwk'))
        self.assertFalse(validate_url('https://google.com/error'))
        self.assertTrue(validate_url('https://google.com'))

    def test_friend_delete_friend(self):
        name = 'wew'
        url = 'https://google.com'
        friend = Friend(name=name, url=url)
        friend.save()

        Friendship(user=self.user_profile, friend=friend).save()

        response = Client().get('/%s/friends/delete_friend/%d/' % (self.username, friend.id))
        html_response = response.content.decode('utf-8')
        self.assertNotIn(name, html_response)
        self.assertNotIn(url, html_response)
    
    def test_friend_add_friend_if_friend_is_already_exist(self):
        name = 'wew'
        url = 'https://google.com'
        friend = Friend(name=name, url=url)
        friend.save()

        Friendship(user=self.user_profile, friend=friend).save()

        data = {'name': name, 'url': url}
        response = Client().post('/%s/friends/add_friend/' % (self.username), data)
        
        response = Client().get('/%s/friends/' % self.username)
        html_response = response.content.decode('utf-8')
        self.assertIn(name, html_response)
        self.assertIn(url, html_response)

class AppFriendFunctional(TestCase):

        username = 'Anonymous'
        user_profile = None
        selenium = None

        def setUp(self):
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

            chrome_options = Options()
            chrome_options.add_argument('--dns-prefetch-disable')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('disable-gpu')
            self.selenium = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)

            super(AppFriendFunctional, self).setUp()

        def tearDown(self):
            self.selenium.quit()
            super(AppFriendFunctional, self).tearDown()

        def test_friend_input_status(self):
            selenium = self.selenium
            # Opening the link we want to test
            selenium.get('http://127.0.0.1:8000/%s/friends/' % (self.username))
            isi_nama = 'namaku ada lima'
            isi_url = 'https://www.google.com'

            name = selenium.find_element_by_id('input-form-name')
            url = selenium.find_element_by_id('input-form-url')
            submit = selenium.find_element_by_id('submit')

            name.send_keys(isi_nama)
            url.send_keys(isi_url)
            # submit
            submit.send_keys(Keys.RETURN)

            # check the returned result
            self.assertIn(isi_nama, selenium.page_source)
            self.assertIn(isi_url, selenium.page_source)

#             # def test_delete_todo(self):
#             #     selenium =./ self.selenium
#             #     DATA = "data-"
#             #     title = 'delete via selenium'
#             #
#             #     todo = Todo.objects.create(title=title, description='test 123 di delete')
#             #     obj_id = todo.id
#             #
#             #     selenium.get('http://127.0.0.1:8000/lab-5/')
#             #     delete = selenium.find_element_by_id(DATA + str(obj_id))
#             #     delete.send_keys(Keys.RETURN)
#             #     self.assertNotIn(title, selenium.page_source)