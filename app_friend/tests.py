from django.test import TestCase
from django.test import Client
from django.urls import resolve
from django.http import HttpRequest
from .models import Friend, Friendship
from .forms import FriendForm
from .views import index,get_query_friends,new_friend



# Create your tests here.

class Lab4UnitTest(TestCase):

    def setUp(self):
        self.user_profile = app_profile_models.UserProfile(
            name=self.username,
            url=self.url ,
        );
        self.user_profile.save()  # save

        super(AppTimelineTest, self).setUp()


    def test_app_friend_url_is_exist(self):
        response = Client().get('/%s/friends/')
        self.assertEqual(response.status_code, 200)


    def test_add_friend_using_index_func(self):
        found = resolve('/%s/friends/')
        self.assertEqual(found.func, index)


    def test_model_can_create_new_friend(self):
        #Creating a new activity
        new_activity = Friends.objects.create(name='seto',url='sbmlagi.herokuapp.com')

        #Retrieving all available activity
        counting_all_available_message= Message.objects.all().count()
        self.assertEqual(counting_all_available_message,1)


    def test_form_validation_for_blank_items(self):
        form = Friend(data={'name': '', 'url': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['url', 'name'],
            ["This field is required."]
        )

    def test_add_friend_fail(self):
        response = Client().post('/%s/friends/', {'name': 'Anonymous', 'url': 'A'})
        self.assertEqual(response.status_code, 302)

    def test_add_friend_success_and_render_the_result(self):
        response = Client().post('/%s/friends/', {'name': '', 'url': ''})
        self.assertEqual(response.status_code, 200)
        html_response = response.content.decode('utf8')
  

    def test_add_friend_showing_all(self):

        name_budi = 'Budi'
        url_budi = 'budi.ui.ac.id'
        data_budi = {'name': name_budi, 'url': url_budi}
        post_data_budi = Client().post('/%s/friends/', data_budi)
        self.assertEqual(post_data_budi.status_code, 302)

        response = Client().get('/%s/friends/')
        html_response = response.content.decode('utf8')

        for key,data in data_budi.items():
            self.assertIn(data,html_response)

    def test_str_message(self):
        new_activity=Friends.objects.create(name=name, url="hehesadf18.com")
        self.assertEqual(str(Friends.objects.all()[0]),"this is a test")