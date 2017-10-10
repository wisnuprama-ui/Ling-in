from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpRequest
from .models import Status
from .views import index, add_status, delete_status, get_queryset
from .forms import StatusPostForm
import app_profile.models as app_profile_models

# Create your tests here.

class AppTimelineTest(TestCase):

    username = 'anon'
    user_profile = None

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

        super(AppTimelineTest, self).setUp()

    def test_timeline_model_status(self):
        model = Status
        content = 'Lorem ipsum dolor sit amet yo yoy'

        # create new activity
        model(user=self.user_profile, content=content).save()

        # check the numbers activity
        counting_all_status = model.objects.all().count()
        self.assertEqual(counting_all_status, 1)

    def test_timeline_model_status_str(self):
        model = Status
        content = 'Lorem ipsum dolor sit amet yo yoy'

        # create activity
        new_status = model(user=self.user_profile, content=content)
        new_status.save()

        test = '%s\n%s' % (self.user_profile.username,
                           content)

        __str__ = new_status.__str__()

        self.assertEqual(test, __str__)

    def test_timeline_get_query(self):

        for i in range(20):
            model = Status
            content = 'Lorem ipsum dolor sit amet yo yoy'

            # create new activity
            model(user=self.user_profile, content=content).save()

        query = get_queryset(self.user_profile)
        self.assertEqual(len(query), model.objects.all().count())

    def test_timeline_url(self):
         url = reverse('app_timeline:timeline_page', args=[self.username])
         self.assertEqual(url, '/%s/timeline/' % (self.username))

         url = reverse('app_timeline:add_status', args=[self.username])
         self.assertEqual(url, '/%s/timeline/add_status/' % (self.username))

    def test_timeline_index_func(self):
        found = resolve('/%s/timeline/' % (self.username))
        self.assertEqual(found.func, index)

    def test_timeline_delete_status_func(self):
        model = Status

        request = HttpRequest()
        test = 'ini content'

        status_delete = model(user=self.user_profile, content=test)
        status_delete.save()

        # data
        id = status_delete.id
        username = self.username

        delete_status(request=request,
                      username=username,
                      status_id=id)

        query = model.objects.filter(pk=id)
        self.assertEqual(len(query), 0)


    def test_timeline_url_respone(self):
        respone = Client().get('/%s/timeline/' % (self.username))
        self.assertEqual(respone.status_code, 200)

    def test_timeline_url_user_not_found_respone(self):
        username = 'iam_username'
        respone = Client().get('/%s/timeline/' % (username))
        self.assertEqual(respone.status_code, 404)

    def test_timeline_form_is_blank_validation(self):
        form = StatusPostForm

        f = form(data={'content': ''})
        self.assertFalse(f.is_valid())
        self.assertEqual(
            f.errors['content'],
            ['This field is required.']
        )

    def test_timeline_post_status_success(self):
        model = Status
        test = 'ini isi content kita'
        response_post = Client().post('/%s/timeline/add_status/' % (self.username),
                                      {'content': test})
        # redirect
        self.assertEqual(response_post.status_code, 302)

        # counting status == 1
        # success
        counting_status = model.objects.all().count()
        self.assertEqual(counting_status, 1)

        # check if there is the status in html respone
        response = Client().get('/%s/timeline/' % (self.username))
        html_response = response.content.decode('utf8')
        self.assertIn(test, html_response)

    def test_timeline_post_error(self):
        test = 'should be error'

        username = self.username
        response_post = Client().post('/%s/timeline/add_status/' % (username),
                                      {'content':''})
        self.assertEqual(response_post.status_code, 302)

        response = Client().get('/%s/timeline/')
        html_response = response.content.decode('utf8')
        self.assertNotIn(test, html_response)
