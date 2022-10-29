from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class PostViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="user")
        cls.group_1 = Group.objects.create(
            title="Тестовая группа 1",
            slug="test1",
            description="Тестовое описание",
        )
        cls.group_2 = Group.objects.create(
            title="Тестовая группа 2",
            slug="test2",
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            text="Тестовый пост", author=cls.user, group=cls.group_1
        )
        cls.url_index = reverse("posts:index")
        cls.url_group_1 = reverse(
            "posts:group_list", kwargs={"slug": cls.group_1.slug}
        )
        cls.url_group_2 = reverse(
            "posts:group_list", kwargs={"slug": cls.group_2.slug}
        )
        cls.url_profile = reverse(
            "posts:profile", kwargs={"username": cls.user.username}
        )
        cls.url_post_detail = reverse(
            "posts:post_detail", kwargs={"post_id": cls.post.id}
        )
        cls.url_post_edit = reverse(
            "posts:post_edit", kwargs={"post_id": cls.post.id}
        )
        cls.url_create_post = reverse("posts:create_post")

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_views_uses_correct_template(self):
        """
        URL-адрес использует соответствующий шаблон
        """
        pages_names_templates = {
            self.url_index: "posts/index.html",
            self.url_group_1: "posts/group_list.html",
            self.url_profile: "posts/profile.html",
            self.url_post_detail: "posts/post_detail.html",
            self.url_post_edit: "posts/create_post.html",
            self.url_create_post: "posts/create_post.html",
        }
        for (
            address,
            template,
        ) in pages_names_templates.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_views_index_context(self):
        """
        Шаблон index сформирован с правильным контекстом
        """
        response = self.authorized_client.get(self.url_index)
        first_post = response.context["page_obj"].object_list[0]
        self.assertEqual(first_post.author, self.user)
        self.assertEqual(first_post, self.post)

    def test_views_context(self):
        """
        Шаблоны group и profile сформированы с правильным контекстом
        """
        urls = [
            self.url_group_1,
            self.url_profile,
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                first_post = response.context["page_obj"].object_list[0]
                self.assertEqual(first_post.author, self.user)
                self.assertEqual(first_post.group, self.group_1)
                self.assertEqual(first_post, self.post)

    def test_views_detail_context(self):
        """
        Шаблон post_detail сформирован с правильным контекстом
        """
        response = self.authorized_client.get(self.url_post_detail)
        self.assertIn("post", response.context)
        self.assertEqual(response.context["post"].author, self.user)
        self.assertEqual(response.context["post"], self.post)

    def test_views_create_context(self):
        """
        Шаблон post_create сформирован с правильным контекстом
        """
        response = self.authorized_client.get(self.url_create_post)
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context["form"].fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_views_edit_context(self):
        """
        Шаблон post_edit сформирован с правильным контекстом
        """
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }

        response = self.authorized_client.get(self.url_post_edit)
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context["form"].fields.get(value)
                self.assertIsInstance(form_field, expected)
        self.assertIn("post", response.context)
        self.assertEqual(response.context["post"].author, self.user)
        self.assertEqual(response.context["post"], self.post)

    def test_group_post_show_correct(self):
        """
        Дополнительная проверка при создании поста
        """
        urls = (
            self.url_index,
            self.url_group_1,
            self.url_profile,
        )
        for address in urls:
            response = self.authorized_client.get(address)
            self.assertIn(self.post, response.context["page_obj"])

        response = self.authorized_client.get(self.url_group_2)
        self.assertNotIn(self.post, response.context["page_obj"])
