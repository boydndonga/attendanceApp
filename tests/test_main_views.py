import unittest
import json
from base64 import b64encode
from app import create_app, db
from app.models import User




class MainViewTESTCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def save_role(self):
        db.session.add(self.new_role)
        db.session.commit()

    @staticmethod
    def get_api_headers(token=''):
        return {
            'Authorization':
                'Basic' + b64encode(('Bearer' + ':' + token).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_client_request(self, path=''):
        return self.client().post(
            path,
            headers=self.get_api_headers(),
            data=json.dumps()
        )


    def test_no_authorization(self):
        res = self.client().get(
            '/api/v1/users'
        )
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],'no Authorization available')
        self.assertEqual(res.status_code, 401)

    def test_empty_authorization(self):
        res = self.client().get(
            '/api/v1/users',
            headers=dict(Authorization="Bearer " + '')
        )
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Authorization is empty')
        self.assertEqual(res.status_code, 401)

    def test_get_users_api(self):
        pass