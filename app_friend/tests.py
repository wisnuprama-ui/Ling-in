# from django.test import TestCase
# from django.test import Client
# from django.urls import resolve
# from django.http import HttpRequest



# # Create your tests here.

# class Lab4UnitTest(TestCase):

#     def setUp(self):
#         self.user_profile = app_profile_models.UserProfile(
#             username=self.username,
#             first_name=self.username,
#             middle_name=self.username,
#             last_name=self.username,
#             email=self.username + '@' + self.username + '.com',
#             birth_date=timezone.now(),
#             birth_place=self.username,
#             gender=app_profile_models.UserProfile.MALE,
#             description=self.username + self.username + self.username
#         );
#         self.user_profile.save()  # save

#         super(AppTimelineTest, self).setUp()


#     def test_app_friend_url_is_exist(self):
#         response = Client().get('/add-friend/')
#         self.assertEqual(response.status_code, 200)


#     def test_add_friend_using_index_func(self):
#         found = resolve('/add-friend/')
#         self.assertEqual(found.func, index)

#     def test_landing_page_is_completed(self):
#         request = HttpRequest()
#         response = index(request)
#         html_response = response.content.decode('utf8')

#         #Checking whether have Bio content
#         self.assertIn(landing_page_content, html_response)

#         #Chceking whether all About Me Item is rendered
#         for item in about_me:
#             self.assertIn(item,html_response) 

#     def test_model_can_create_new_friend(self):
#         #Creating a new activity
#         new_activity = Fr.objects.create(name='seto',url='sbmlagi.herokuapp.com')

#         #Retrieving all available activity
#         counting_all_available_message= Message.objects.all().count()
#         self.assertEqual(counting_all_available_message,1)

#     def test_form_message_input_has_placeholder_and_css_classes(self):
#         form = Message_Form()
#         self.assertIn('class="form-control"', form.as_p())
#         self.assertIn('<label for="id_name">Nama:</label>', form.as_p())
#         self.assertIn('<label for="id_url">Email:</label>', form.as_p())

#     def test_form_validation_for_blank_items(self):
#         form = Message_Form(data={'name': '', 'url': ''})
#         self.assertFalse(form.is_valid())
#         self.assertEqual(
#             form.errors['url', 'name'],
#             ["This field is required."]
#         )

#     def test_add_friend_post_fail(self):
#         response = Client().post('/add_friend', {'name': 'Anonymous', 'url': 'A'})
#         self.assertEqual(response.status_code, 302)

#     def test_lab4_post_success_and_render_the_result(self):
#         response = Client().post('/add_friend', {'name': '', 'url': ''})
#         self.assertEqual(response.status_code, 200)
#         html_response = response.content.decode('utf8')
  

#     def test_lab_4_showing_all_messages(self):

#         name_budi = 'Budi'
#         url_budi = 'budi.ui.ac.id'
#         data_budi = {'name': name_budi, 'url': url_budi}
#         post_data_budi = Client().post('/add_friend', data_budi)
#         self.assertEqual(post_data_budi.status_code, 200)

#         response = Client().get('/lab-4/result_table')
#         html_response = response.content.decode('utf8')

#         for key,data in data_budi.items():
#             self.assertIn(data,html_response)

#     def test_str_message(self):
#         new_activity=Message.objects.create(name=mhs_name, email="hehesadf18.com")
#         self.assertEqual(str(Message.objects.all()[0]),"this is a test")