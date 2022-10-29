from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Group, Post, User


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostForm()
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

    def test_create_post_as_user(self):
        """
        При отправке валидной формы создаётся новая запись в базе данных
        """
        posts_count = Post.objects.count()
        form_data = {"text": self.post.text, "group": self.group.id}
        response = self.authorized_client.post(
            reverse("posts:create_post"), data=form_data, follow=True
        )
        first_post = Post.objects.first()
        self.assertRedirects(
            response,
            reverse("posts:profile", kwargs={"username": self.user.username}),
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(first_post.text, self.post.text)
        self.assertEqual(first_post.group, self.post.group)
        self.assertEqual(first_post.author, self.post.author)

    def test_post_edit_as_user(self):
        """
        При редактировании существующего поста изменяется
        соответствующая ему запись в базе данных
        """
        form_data = {"text": "Измененный пост"}
        response = self.authorized_client.post(
            reverse(
                "posts:post_edit",
                kwargs={"post_id": self.post.id},
            ),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("posts:post_detail", kwargs={"post_id": self.post.id}),
        )
        self.assertTrue(
            Post.objects.filter(
                text="Измененный пост", id=self.post.id
            ).exists()
        )

    def test_post_create_as_guest(self):
        """
        Проверка анонимных клиентов на возможность создания новых записей
        """
        posts_count = Post.objects.count()
        form_data = {"text": self.post.text, "group": self.group.id}
        response = self.guest_client.post(
            reverse("posts:create_post"), data=form_data, follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertEqual(response.status_code, HTTPStatus.OK)
