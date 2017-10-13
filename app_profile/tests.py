from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpRequest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ErrorInResponseException
from .views import index, edit
from .models import UserProfile,Expertise,ExpertIn, user_directory_img_path

class ProfileUnitTest(TestCase):

    def setUp(self):
        self.username = 'Anonymous'
        self.user_profile = UserProfile(
            username=self.username,
            first_name=self.username,
            middle_name=self.username,
            last_name=self.username,
            email=self.username + '@' + self.username + '.com',
            birth_date=timezone.now(),
            birth_place=self.username,
            gender=UserProfile.MALE,
            description=self.username + self.username + self.username
        );
        self.user_profile.save()  # save

        super(ProfileUnitTest, self).setUp()


    def test_profile_models(self):
        expert = Expertise(expertise='main bola')
        expert.save()

        self.assertEqual(
            Expertise.objects.all().count(), 1
        )

        self.assertEqual(
            UserProfile.objects.all().count(), 1
        )

        exp = ExpertIn(user=self.user_profile, expertise=expert)
        exp.save()

        self.assertEqual(ExpertIn.objects.all().count(), 1)

        self.assertEqual(self.username, self.user_profile.__str__())


    def test_profile_url(self):
        url = reverse('app_profile:profile_page', args=[self.username ])
        self.assertEqual(url, '/%s/' % self.username)


    def test_url_profile_is_exist(self):
        response= Client().get('/%s/' % self.username)
        self.assertEqual(response.status_code, 200)


    def test_profile_using_index_func(self):
        found = resolve('/%s/' % self.username)
        self.assertEqual(found.func, index)

    def test_profile_user_expertise_in_profile_page(self):
        exp = Expertise(expertise='ngoding')
        exp.save()

        exp_in = ExpertIn(user=self.user_profile, expertise=exp)
        exp_in.save()

        found = resolve('/%s/' % self.username)
        self.assertEqual(found.func, index)

        response = Client().get('/%s/' % self.username)
        html_resp = response.content.decode('utf-8')
        self.assertIn(exp.expertise, html_resp)
    
    def test_profile_check_dir_image_profile(self):
        test = 'image/user/%s/profile/%s' % (self.username, 'ohyeah')
        res = user_directory_img_path(self.user_profile, 'ohyeah')
        wa = user_directory_img_path(self.user_profile, 'noimage')

        self.assertEqual(test, res)
        self.assertNotEqual(test, wa)

    def test_profile_edited_using_edit_func(self):
        # temporary. find the solution when create edit profile
        edit(HttpRequest(), username=self.username)

