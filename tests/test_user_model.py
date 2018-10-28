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
        self.new_user = User(username='boyde', email='boyde@gmaile.com', pass_secure='walaisijui', role= self.new_role)
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

    def test_email_validator(self):
        # testvalid email
        email = self.new_user.validate_email()
        self.assertTrue(email)

        #test invalid email
        u2 = User(username='boyde', email='boyde@gmaile.cm', pass_secure='walaisijui', role= self.new_role)
        email2 = u2.validate_email()
        self.assertFalse(email2)

    def test_password_validator(self):
        #test invalid password
        user = User(username='boyde', email='boyde@gmaile.cm', pass_secure='pswd', role=self.new_role)
        pass2 = user.validate_password()
        self.assertFalse(pass2)

        # test empty password
        user = User(username='boyde', email='boyde@gmaile.cm', pass_secure='', role=self.new_role)
        pass2 = user.validate_password()
        self.assertFalse(pass2)

        #test valid password
        user = User(username='boyde', email='boyde@gmaile.cm', pass_secure='cdb3t3nkj56', role=self.new_role)
        pass2 = user.validate_password()
        self.assertTrue(pass2)


    def test_save_user(self):
        db.session.add(self.new_user)
        db.session.commit()
        self.assertTrue(len(User.query.all()) > 0)

    def test_email_verification(self):
        db.session.add(self.new_user)
        db.session.commit()
        verified_email = self.new_user.verify_email()
        self.assertTrue(verified_email)

    def test_user_has_role(self):
        db.session.add(self.new_role)
        db.session.commit()
        db.session.add(self.new_user)
        db.session.commit()
        person = User.query.filter_by(username='boyde').first()
        self.assertEqual(person.role_id, self.new_role.id)