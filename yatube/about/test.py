from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class AboutUrlTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_urls(self):
        """
        Проверка доступности страниц и названий шаблонов
        """
        urls = {
            reverse("about:author"): "about/author.html",
            reverse("about:tech"): "about/tech.html",
        }
        for address, template in urls.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)
