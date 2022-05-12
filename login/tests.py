import unittest
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginTestCase(unittest.TestCase):
    def test_login(self):
        user=User.objects.create_user("user1","","user1")
        user.save()
        user=authenticate(username="user1",password="user1")
        self.assertEqual(user.is_authenticated(),True)
if __name__ == '__main__':
    unittest.main()
