# from django.test import TestCase

# Create your tests here.
# class Lab5UnitTest(TestCase):
#     def test_url_is_exist(self):
#         response = Client().get('/stats/)
#         self.assertEqual(response.status_code, 200)

#     def test_using_index_func(self):
#         found = resolve('/stats/')
#         self.assertEqual(found.func, index)
    
#     def test_ada_navbar(self):
#         response = Client().get('/stats/')
#         html_response = response.content.decode('utf8')
#         self.assertIn('<nav',html_response)
    
#     def test_ada_copyright(self):
#         response = Client().get('/stats/')
#         html_response = response.content.decode('utf8')
#         self.assertIn('&copy;', html_response)
    
#     