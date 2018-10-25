import unittest
from app import create_app,db
from app.models import User, Role


class UserModelTESTCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client
        self.new_role = Role(name='Admin')
        self.new_user = User(username='boyde', email='boyde@gmaile.com', password='walaisijui', role_id= self.new_role)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_instance_var(self):
        self.assertEqual(self.new_user.username, 'boyde')
        self.assertEqual(self.new_user.email, 'boyde@gmaile.com')

    def test_no_password_getter(self):
        with self.assertRaises(AttributeError):
            self.new_user.password()

    def test_save_user(self):
        db.session.add(self.new_user)
        db.session.commit()
        self.assertTrue(len(User.query.all()) > 0)