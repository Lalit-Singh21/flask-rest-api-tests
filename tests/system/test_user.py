from models.user import UserModel
from tests.base_test import BaseTest
import json

class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={
                    'username': 'test',
                    'password': '1234'
                })
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({"message": "User created successfully."},
                                     json.loads(response.data))

    def test_register_and_login(self):
        uid_dict = {'username': 'test', 'password': '1234'}
        with self.app() as c:
            with self.app_context():
                c.post('/register', data=uid_dict)
                auth_response = c.post('/auth', data=json.dumps(uid_dict), headers={'Content-Type': 'application/json'})

                self.assertIn('access_token', json.loads(auth_response.data).keys())

    def test_register_duplicate_user(self):
        uid_dict = {'username': 'test', 'password': '1234'}
        with self.app() as c:
            with self.app_context():
                c.post('/register', data=uid_dict)
                response = c.post('/register', data=uid_dict)
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({"message": "A user with that username already exists"},
                                     json.loads(response.data))

