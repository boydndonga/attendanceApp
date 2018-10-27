import unittest
from app import create_app,db
from app.models import Role, User


class RoleModelTESTCase(unittest.TestCase):
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

    def test_role_instance_var(self):
        self.assertEqual(self.new_role.name, 'Admin')

    def test_save_role(self):
        db.session.add(self.new_role)
        db.session.commit()
        self.assertTrue(len(Role.query.all()) > 0)

    def test_role_has_users(self):
        new_user = User(username='boyde', email='boyde@gmaile.com', pass_secure='walaisijui', role= self.new_role)
        db.session.add(new_user)
        db.session.commit()
        self.assertTrue(len(self.new_role.users) > 0)