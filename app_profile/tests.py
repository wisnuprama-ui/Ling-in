from django.test import TestCase
from django.test import Client
from .views import index, edit

class ProfileUnitTest(TestCase):

	def test_url_profile_is_exist(self):
		response= Clent().get('/app_profile/')
		self.assertEqual(response.status_code, 200)

	def test_profile_using_index_func(self):
		found = resolve('app_profile:profile_page')
		self.assertTrue(found.func, index)

	#def test_profile_edited_using_edit_func(self):


