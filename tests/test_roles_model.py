import unittest
from app import create_app,db
from app.models import Role


class UserModelTESTCase(unittest.TestCase):
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

    def test_save_role(self):
        self.assertEqual(self.new_role.name, 'Admin')