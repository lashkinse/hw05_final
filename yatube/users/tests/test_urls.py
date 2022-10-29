from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from posts.models import User


class UserUrlTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="user")

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_as_guest(self):
        """
        Проверка доступности страниц и названий шаблонов для
        анонимных пользователей
        """
        urls = {
            reverse("users:signup"): "users/signup.html",
            reverse("users:login"): "users/login.html",
            reverse("users:password_reset"): "users/password_reset_form.html",
            reverse(
                "users:password_reset_done"
            ): "users/password_reset_done.html",
            reverse(
                "users:password_reset_confirm",
                kwargs={"uidb64": "1", "token": "123qwerty"},
            ): "users/password_reset_confirm.html",
            reverse(
                "users:password_reset_complete"
            ): "users/password_reset_complete.html",
        }
        for address, template in urls.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)

    def test_urls_as_user(self):
        """
        Проверка доступности страниц и названий шаблонов для
        авторизованных пользователей
        """
        urls = {
            reverse(
                "users:password_change"
            ): "users/password_change_form.html",
            reverse(
                "users:password_change_done"
            ): "users/password_change_done.html",
            reverse("users:logout"): "users/logged_out.html",
        }
        for address, template in urls.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)
