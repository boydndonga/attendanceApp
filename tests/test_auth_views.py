# import unittest
# import json
# from base64 import b64encode
# from app import create_app
#
#
# class AuthViewTESTCase(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app('testing')
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         self.client = self.app.test_client
#
#     @staticmethod
#     def get_api_headers(email='', password=''):
#         return {
#             'Authorization':
#                 'Basic' + b64encode((email + ':' + password).encode('utf-8')).decode('utf-8'),
#             'Accept': 'application/json',
#             'Content-Type': 'application/json'
#         }
#
#     def get_client_request(self, email='app@test.com', password='appytesty', path='/authenticate/register'):
#         user_data = {'email': email, 'password': password}
#         return self.client().post(
#             path,
#             headers=self.get_api_headers(),
#             data=json.dumps(user_data)
#         )