import asyncio
from unittest import TestCase
from fastapi.testclient import TestClient
from fastapi_jwt_auth.auth_jwt import AuthJWT

from tortoise.contrib.test import finalizer, initializer


from app.models.user import User
from app.main import app
from app.utils.security import create_tokens
from app import settings

loop = asyncio.get_event_loop()

base_client = TestClient(app)

async def create_user(email: str, domain: str = "testserver", password: str = "test") -> User:
    user = User(email=email, domain=domain)
    user.set_password(password)
    await user.save()
    return user


class TestJwtAuthorization(TestCase):
    PASSWORD = 'test'

    def setUp(self) -> None:
        initializer(settings.MODELS)
        self.user = loop.run_until_complete(
            create_user('test@dev.com', password=self.PASSWORD)
        )
        self.tokens = create_tokens(
            AuthJWT(),
            self.user.id,
            email = self.user.email,
            domain = self.user.domain,
        )
    
    def tearDown(self) -> None:
        finalizer()

    def test_register_user_200_ok(self):
        user_data = {
            'email': 'test2@dev.com',
            'password1': self.PASSWORD,
            'password2': self.PASSWORD,
        }
        response = base_client.post(
            '/register',
            json = user_data
        )
        self.assertEqual(response.status_code, 200)

    def test_register_user_422_already_exist(self):
        user_data = {
            'email': 'test@dev.com',
            'password1': self.PASSWORD,
            'password2': self.PASSWORD,
        }
        response = base_client.post(
            '/register',
            json = user_data
        )
        self.assertEqual(response.status_code, 422)

    def test_register_from_different_domain_200_ok(self):
        user_data = {
            'email': 'test@dev.com',
            'password1': self.PASSWORD,
            'password2': self.PASSWORD,
        }
        client = TestClient(app, 'http://testdomain')
        response = client.post(
            '/register',
            json = user_data
        )
        self.assertEqual(response.status_code, 200)

    def test_register_with_different_passwords_422(self):
        user_data = {
            'email': 'testdiff@dev.com',
            'password1': self.PASSWORD+'dummy',
            'password2': self.PASSWORD,
        }
        response = base_client.post(
            '/register',
            json = user_data
        )
        self.assertEqual(response.status_code, 422)
    
    def test_login_200_ok(self):
        login_data = {
            'email': self.user.email,
            'password': self.PASSWORD
        }
        response = base_client.post(
            '/login',
            json = login_data,
        )
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data['access_token'])
        self.assertTrue(response_data['refresh_token'])

    def test_login_wrong_email_400(self):
        login_data = {
            'email': 'notexist@test.com',
            'password': self.PASSWORD
        }
        response = base_client.post(
            '/login',
            json = login_data,
        )
        self.assertEqual(response.status_code, 400)
    
    def test_login_wrong_password_400(self):
        login_data = {
            'email': self.user.email,
            'password': self.PASSWORD + 'wrong'
        }
        response = base_client.post(
            '/login',
            json = login_data,
        )
        self.assertEqual(response.status_code, 400)

    def test_login_wrong_domain_400(self):
        login_data = {
            'email': self.user.email,
            'password': self.PASSWORD
        }
        client = TestClient(app, 'http://testdomain')
        response = client.post(
            '/login',
            json = login_data,
        )
        self.assertEqual(response.status_code, 400)
    
    def test_refresh_tokens_200_ok(self):
        client = TestClient(app)
        token = self.tokens.refresh_token
        client.headers['Authorization'] = f'Bearer {token}'
        response = client.get('/refresh')
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data['access_token'])
        self.assertTrue(response_data['refresh_token'])
    
    def test_refresh_tokens_not_authenticated_403(self):
        response = base_client.get('/refresh')
        self.assertEqual(response.status_code, 403)

    def test_security_test_200_ok(self):
        client = TestClient(app)
        token = self.tokens.access_token
        client.headers['Authorization'] = f'Bearer {token}'
        response = client.get('/api/security_test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

    def test_security_test_wrong_domain_401(self):
        client = TestClient(app, 'http://wrongdomain')
        token = self.tokens.access_token
        client.headers['Authorization'] = f'Bearer {token}'
        response = client.get('/api/security_test')
        self.assertEqual(response.status_code, 401)
    
    def test_security_test_not_authenticated_403(self):
        response = base_client.get('/api/security_test')
        self.assertEqual(response.status_code, 403)
    