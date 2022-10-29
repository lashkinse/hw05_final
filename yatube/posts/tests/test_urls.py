from http import HTTPStatus

from django.test import Client, TestCase

from posts.models import Group, Post, User


class PostUrlTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="user")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test",
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            text="Тестовый пост", author=cls.user, group=cls.group
        )

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
            "/": "posts/index.html",
            f"/group/{self.group.slug}/": "posts/group_list.html",
            f"/profile/{self.user.username}/": "posts/profile.html",
            f"/posts/{self.post.id}/": "posts/post_detail.html",
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
            "/create/": "posts/create_post.html",
            f"/posts/{self.post.id}/edit/": "posts/create_post.html",
        }
        for address, template in urls.items():
            with self.subTest(address=address):
                response_user = self.authorized_client.get(address)
                self.assertEqual(response_user.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response_user, template)
                response_guest = self.guest_client.get(address)
                self.assertRedirects(
                    response_guest, f"/auth/login/?next={address}"
                )

    def test_unexisting_page(self):
        """
        Проверка доступа к несуществующей странице
        """
        response = self.guest_client.get("/unexisting_page/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
