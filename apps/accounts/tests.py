"""python manage.py test apps.accounts   (10-апта: тіркелу және профиль)"""
import base64

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()
BASE = "/api/drf/auth"
GOOD = {"username": "newbie", "email": "newbie@example.com", "password": "Strong#Pass2026"}


def basic(username, password):
    return "Basic " + base64.b64encode(f"{username}:{password}".encode()).decode()


class RegistrationTests(APITestCase):
    def setUp(self):
        User.objects.create_user("existing", "existing@example.com", "Existing#Pass1")

    def test_register_hashes_password(self):
        resp = self.client.post(f"{BASE}/register/", GOOD, format="json")
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertNotIn("password", resp.data)
        user = User.objects.get(username="newbie")
        self.assertNotEqual(user.password, GOOD["password"])          # ашық мәтін емес
        self.assertTrue(user.password.startswith("pbkdf2_"))           # хеш
        self.assertTrue(user.check_password(GOOD["password"]))

    def test_duplicate_username_is_rejected(self):
        for name in ("existing", "EXISTING"):                           # регистрге қарамай
            resp = self.client.post(f"{BASE}/register/", dict(GOOD, username=name), format="json")
            self.assertEqual(resp.status_code, 400)
            self.assertIn("username", resp.data)

    def test_invalid_data_is_rejected(self):
        self.assertEqual(self.client.post(f"{BASE}/register/", {}, format="json").status_code, 400)
        bad_email = dict(GOOD, email="not-an-email")
        self.assertEqual(self.client.post(f"{BASE}/register/", bad_email, format="json").status_code, 400)
        short = dict(GOOD, password="123")
        self.assertEqual(self.client.post(f"{BASE}/register/", short, format="json").status_code, 400)
        self.assertFalse(User.objects.filter(username="newbie").exists())

    def test_me_requires_authentication(self):
        self.assertEqual(self.client.get(f"{BASE}/me/").status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION=basic("existing", "wrong-password"))
        self.assertEqual(self.client.get(f"{BASE}/me/").status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION=basic("existing", "Existing#Pass1"))
        resp = self.client.get(f"{BASE}/me/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["username"], "existing")
        self.assertNotIn("password", resp.data)
