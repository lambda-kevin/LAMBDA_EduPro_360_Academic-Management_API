# users/tests.py
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class LoginTests(APITestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            correo="testuser@example.com",
            nombre="Test",
            apellido="User",
            password="TestPass123!"
        )
        self.url = reverse('login')

    def test_login_ok(self):
        data = {"correo": "testuser@example.com", "password": "TestPass123!"}
        resp = self.client.post(self.url, data, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn("tokens", resp.data)
        self.assertIn("access", resp.data["tokens"])
        self.assertIn("refresh", resp.data["tokens"])

    def test_login_bad_password(self):
        data = {"correo": "testuser@example.com", "password": "WrongPass"}
        resp = self.client.post(self.url, data, format='json')
        self.assertEqual(resp.status_code, 400)
