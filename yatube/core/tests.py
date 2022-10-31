from http import HTTPStatus

from django.test import Client, TestCase

from posts.models import User


class CoreTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="user")

    def setUp(self):
        self.guest_client = Client()

    def test_unexisting_page(self):
        """
        Проверка доступа к несуществующей странице
        """
        response = self.guest_client.get("/unexisting_page/")
        self.assertTemplateUsed(response, "core/404.html")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
