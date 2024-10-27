import unittest
from email_func_app import create_app, db
from email_func_app.models import User
from flask_testing import TestCase
from werkzeug.security import generate_password_hash

class TestApp(TestCase):
    def create_app(self):
        # Configure the app with testing settings
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        return app

    def setUp(self):
        with self.app.app_context():
            db.create_all()
            # Add a test user with a hashed password
            user = User(
                email='test@example.com',
                password=generate_password_hash('password'),
                user_type='influencer'
            )
            db.session.add(user)
            db.session.commit()
            self.test_user = user

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login_user(self, email, password):
        return self.client.post('/login', data={
            'email': email,
            'password': password,
        }, follow_redirects=True)

    def test_index_route(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assertIn('بلاگرز', response.get_data(as_text=True))

    def test_register_route_get(self):
        response = self.client.get('/register')
        self.assert200(response)
        self.assertIn('ایجاد حساب کاربری جدید', response.get_data(as_text=True))

    def test_login_route_get(self):
        response = self.client.get('/login')
        self.assert200(response)
        self.assertIn('ورود به حساب کاربری', response.get_data(as_text=True))

    def test_register_route_post(self):
        response = self.client.post('/register', data={
            'email': 'newuser@example.com',
            'password': 'password',
            'confirm_password': 'password',
            'user_type': 'influencer',
            # Include required fields for influencer
            'influencer_social_media': 'instagram.com/newuser',
            'influencer_followers': '5000',
            'basic_profile_info': 'New influencer profile info.',
            'submit': True
        }, follow_redirects=True)
        self.assert200(response)
        self.assertIn('داشبورد', response.get_data(as_text=True))

    def test_login_route_post(self):
        response = self.login_user('test@example.com', 'password')
        self.assert200(response)
        self.assertIn('داشبورد', response.get_data(as_text=True))

    def test_dashboard_access_without_login(self):
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assert200(response)
        self.assertIn('ورود به حساب کاربری', response.get_data(as_text=True))

    def test_logout(self):
        # Log in as test user
        self.login_user('test@example.com', 'password')
        # Logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assert200(response)
        self.assertIn('شما با موفقیت خارج شدید.', response.get_data(as_text=True))
        # Try to access dashboard
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assert200(response)
        self.assertIn('ورود به حساب کاربری', response.get_data(as_text=True))

    def test_settings_update(self):
        # Log in as test user
        self.login_user('test@example.com', 'password')
        # Update settings
        response = self.client.post('/settings', data={
            'instagram_profile': 'updated_profile',
            'influencer_social_media': 'Instagram',
            'influencer_followers': '10000',
            'name': 'Updated Name',
            'phone_number': '1234567890',
            'social_links': 'https://instagram.com/updated',
            'bio': 'Updated bio',
            'services_interested_in': 'Travel, Fashion',
        }, follow_redirects=True)
        self.assert200(response)
        self.assertIn('تغییرات با موفقیت ذخیره شد.', response.get_data(as_text=True))

    def test_404_error_handling(self):
        response = self.client.get('/nonexistentpage')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
