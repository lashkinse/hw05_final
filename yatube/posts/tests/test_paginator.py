from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, User


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="user")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test",
            description="Тестовое описание",
        )
        Post.objects.bulk_create(
            [
                Post(
                    text=f"Тестовый пост номер{str(i)}",
                    author=cls.user,
                    group=cls.group,
                )
                for i in range(13)
            ]
        )
        cls.urls = (
            reverse("posts:index"),
            reverse("posts:group_list", kwargs={"slug": cls.group.slug}),
            reverse("posts:profile", kwargs={"username": cls.user.username}),
        )

    def setUp(self):
        self.guest_client = Client()

    def test_first_page_contains_ten_records(self):
        """
        Проверка: количество постов на первой странице равно 10
        """
        for address in self.urls:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(
                    len(response.context.get("page_obj").object_list), 10
                )

    def test_second_page_contains_three_records(self):
        """
        Проверка: на второй странице должно быть три поста
        """
        for address in self.urls:
            with self.subTest(address=address):
                response = self.guest_client.get(address + "?page=2")
                self.assertEqual(
                    len(response.context.get("page_obj").object_list), 3
                )
