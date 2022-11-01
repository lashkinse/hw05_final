from django.test import Client, TestCase
from django.urls import reverse
from posts.models import User


class UserFormTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_create_user(self):
        """
        При заполнении формы reverse('users:signup') создаётся
        новый пользователь
        """
        user_count = User.objects.count()
        form_data = {
            "first_name": "new_user",
            "last_name": "new_user",
            "username": "new_user",
            "email": "new_user@mail.ru",
            "password1": "12qwaszxQWASZX",
            "password2": "12qwaszxQWASZX",
        }
        response = self.guest_client.post(
            reverse("users:signup"),
            data=form_data,
        )
        self.assertRedirects(response, reverse("posts:index"))
        self.assertEqual(User.objects.count(), user_count + 1)
        self.assertTrue(User.objects.get(username="new_user"))
