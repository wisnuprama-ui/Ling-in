from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpRequest
from .models import Status, Comment
from .views import index, add_status, delete_status, get_queryset, StatusComment, index_comment
from .forms import StatusPostForm
import app_profile.models as app_profile_models
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ErrorInResponseException
from selenium.webdriver.common.by import By

# Create your tests here.

class AppTimelineTest(TestCase):

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

        super(AppTimelineTest, self).setUp()

    def test_timeline_model_status(self):
        model = Status
        content = 'Lorem ipsum dolor sit amet yo yoy'

        # create new activity
        model(user=self.user_profile, content=content).save()

        # check the numbers activity
        counting_all_status = model.objects.count()
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
        self.assertEqual(len(query), model.objects.count())

    def test_timeline_url(self):
        url = reverse('app_timeline:timeline_page', args=[self.username])
        self.assertEqual(url, '/%s/timeline/' % (self.username))

        url = reverse('app_timeline:add_status', args=[self.username])
        self.assertEqual(url, '/%s/timeline/add_status/' % (self.username))
        
        url = reverse('app_timeline:delete_status', args=[self.username, 0])
        self.assertEqual(url, '/%s/timeline/delete/%d/'%(self.username, 0))

        url = reverse('app_timeline:comment', args=[self.username, 0])
        self.assertEqual(url, '/%s/timeline/comment/%d/'%(self.username, 0))

        url = reverse('app_timeline:comment_status', args=[self.username, 0])
        self.assertEqual(url, '/%s/timeline/comment/%d/post_comment/'%(self.username, 0))

    def test_timeline_index_func(self):
        found = resolve('/%s/timeline/' % (self.username))
        self.assertEqual(found.func, index)
    
    def test_timeline_index_comment_func(self):
        found = resolve('/%s/timeline/comment/%d/' % (self.username, 0))
        self.assertEqual(found.func, index_comment)
        
        content = 'Lorem ipsum dolor sit amet yo yoy'
        new_status = Status(user=self.user_profile, content=content)
        new_status.save()

        response = index_comment(HttpRequest(), username=self.user_profile, status_id=new_status.id)
        html_response = response.content.decode('utf-8')
        self.assertIn('Comment', html_response)
        self.assertIn(new_status.content, html_response)

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
        counting_status = model.objects.count()
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

        response = Client().get('/%s/timeline/' % self.username)
        html_response = response.content.decode('utf8')
        self.assertNotIn(test, html_response)
    
    def test_timeline_post_comment_success(self):
        model = Comment
        test = 'ini isi content kita'
        status = Status(user=self.user_profile, content=test)
        status.save()

        response_post = Client().post('/%s/timeline/comment/%d/post_comment/' % (self.username, status.id),
                                      {'content': test})
        # redirect
        self.assertEqual(response_post.status_code, 302)

        counting_comment = model.objects.count()
        self.assertEqual(counting_comment, 1)

        # check if there is the status in html respone
        response = Client().get('/%s/timeline/' % (self.username))
        html_response = response.content.decode('utf8')
        self.assertIn(test, html_response)

    def test_timeline_comment_error(self):
        test = 'well done body'
        status = Status(user=self.user_profile, content='blabla')
        status.save()

        response_post = Client().post('/%s/timeline/comment/%d/post_comment/' % (self.username, status.id),
                                      {'content':''})
        self.assertEqual(response_post.status_code, 302)

        response = Client().get('/%s/timeline/' % self.username)
        html_response = response.content.decode('utf8')
        self.assertNotIn(test, html_response)
    
    def test_timeline_models_comment(self):
        status = Status(user=self.user_profile, content='behehehe')
        status.save()
        comment = Comment(
            user=self.user_profile,
            status=status,
            content='behehehe')
        comment.save()

        _str_ = '%s: %s - %s' % (status, self.user_profile, comment.content)

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(comment.__str__(), _str_)

    def test_timeline_statuscomment(self):
        status = Status(user=self.user_profile, content='behehehe')
        status.save()
        status_comment = StatusComment(status=status)
        
        test = '%s: %d' % (status, 0)

        self.assertEqual(test, status_comment.__str__())
        self.assertEqual(test, status_comment.__repr__())

    def test_timeline_query_status_more_than_50(self):
        st = None
        for i in range(51):
            st = Status(user=self.user_profile, content='behehe')
            st.save()

        for i in range(11):
            Comment(user=self.user_profile, status=st, content='behehe2').save()
        
        query = get_queryset(self.user_profile)

        target_sc = None
        for sc in query:
            if(sc.status==st):
                target_sc = sc
                break;

        self.assertEqual(len(query), 50)
        self.assertEqual(len(target_sc.comment), 10)
    



class AppTimelineFunctional(TestCase):

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
        )
        self.user_profile.save()  # save

        chrome_options = Options()
        chrome_options.add_argument('--dns-prefetch-disable')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('disable-gpu')
        self.selenium = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)

        super(AppTimelineFunctional, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AppTimelineFunctional, self).tearDown()

    def test_timeline_input_status(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get('http://127.0.0.1:8000/%s/timeline/' % (self.username))
        isi_status = 'ini statusku, kalo kamu?'

        self.selenium.find_element_by_id('status-form-textarea').click()
        status = selenium.find_element_by_id('status-form-textarea')
        submit = selenium.find_element_by_id('submit')
        status.send_keys(isi_status)

        # submit
        submit.send_keys(Keys.RETURN)

        # check the returned result
        self.assertIn(isi_status, selenium.page_source)

    # def test_delete_todo(self):
    #     selenium = self.selenium
    #     DATA = "data-"
    #     title = 'delete via selenium'
    #
    #     todo = Todo.objects.create(title=title, description='test 123 di delete')
    #     obj_id = todo.id
    #
    #     selenium.get('http://127.0.0.1:8000/lab-5/')
    #     delete = selenium.find_element_by_id(DATA + str(obj_id))
    #     delete.send_keys(Keys.RETURN)
    #     self.assertNotIn(title, selenium.page_source)