import unittest
import json
from base64 import b64encode
from app import create_app, db
from app.models import Role, User


class AuthViewTESTCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client
        self.new_role = Role(name='Admin')
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def save_role(self):
        db.session.add(self.new_role)
        db.session.commit()

    @staticmethod
    def get_api_headers(email='', password=''):
        return {
            # 'Authorization':
            #     'Basic' + b64encode((email + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_client_request(self, username='testsy', email='app@test.com', password='appytesty', path='/authenticate/register'):
        user_data = {'username':username, 'email': email, 'password': password}
        return self.client().post(
            path,
            headers=self.get_api_headers(),
            data=json.dumps(user_data)
        )

    def test_auth_registration(self):
        # test registration has no get request
        user_data = {'username':'testsy', 'email': 'app@test.com', 'password': 'appytesty'}
        res = self.client().get(
            '/authenticate/register',
            headers=self.get_api_headers(),
            data=json.dumps(user_data)
        )
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid request')
        self.assertEqual(res.status_code, 404)

        # test successful registration
        res = self.get_client_request()
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'successfully created user')
        self.assertEqual(res.status_code, 201)

        # test invalid email
        res = self.get_client_request(email='app@test.cm')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'invalid email')
        self.assertEqual(res.status_code, 403)