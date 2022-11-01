import shutil
import tempfile

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.models import Follow, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="user")
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )
        uploaded = SimpleUploadedFile(
            name="small.gif", content=small_gif, content_type="image/gif"
        )
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
            text="Тестовый пост",
            author=cls.user,
            group=cls.group_1,
            image=uploaded,
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

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        cache.clear()
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
        self.assertIn("page_obj", response.context)
        post = response.context["page_obj"].object_list[0]
        self.assertEqual(post.author, self.post.author)
        self.assertEqual(post.group, self.post.group)
        self.assertEqual(post.image, self.post.image)

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
                self.assertIn("page_obj", response.context)
                post = response.context["page_obj"].object_list[0]
                self.assertEqual(post.author, self.post.author)
                self.assertEqual(post.group, self.post.group)
                self.assertEqual(post.image, self.post.image)

    def test_views_detail_context(self):
        """
        Шаблон post_detail сформирован с правильным контекстом
        """
        response = self.authorized_client.get(self.url_post_detail)
        self.assertIn("post", response.context)
        post = response.context["post"]
        self.assertEqual(post.author, self.post.author)
        self.assertEqual(post.group, self.post.group)
        self.assertEqual(post.image, self.post.image)

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
                self.assertIn("form", response.context)
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
                self.assertIn("form", response.context)
                form_field = response.context["form"].fields.get(value)
                self.assertIsInstance(form_field, expected)
        self.assertIn("post", response.context)
        post = response.context["post"]
        self.assertEqual(post.author, self.post.author)
        self.assertEqual(post.group, self.post.group)
        self.assertEqual(post.image, self.post.image)

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
            self.assertIn("page_obj", response.context)
            self.assertIn(self.post, response.context["page_obj"])

        response = self.authorized_client.get(self.url_group_2)
        self.assertIn("page_obj", response.context)
        self.assertNotIn(self.post, response.context["page_obj"])


class PostCacheTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="user")
        cls.post = Post.objects.create(
            text="Тестовый пост",
            author=cls.user,
        )

    def setUp(self):
        self.guest_client = Client()

    def test_index_cache(self):
        """
        Тестирование кэша
        """
        posts_count = Post.objects.count()
        response = self.guest_client.get(reverse("posts:index"))
        cached_content = response.content
        self.post.delete()
        self.assertEqual(Post.objects.count(), posts_count - 1)
        response = self.guest_client.get(reverse("posts:index"))
        self.assertIn(cached_content, response.content)
        cache.clear()
        response = self.guest_client.get(reverse("posts:index"))
        self.assertNotEqual(cached_content, response.content)


class PostFollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="user")
        cls.author = User.objects.create_user(username="author")
        cls.unfollower = User.objects.create_user(username="unfollower")
        cls.post = Post.objects.create(
            author=cls.author,
            text="Тестовый пост",
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.unfollower_client = Client()
        self.unfollower_client.force_login(self.unfollower)

    def test_follow_as_user(self):
        """
        Пользователь может подписываться на других пользователей
        """
        follow_count = Follow.objects.count()
        response = self.authorized_client.post(
            reverse(
                "posts:profile_follow",
                kwargs={"username": self.author.username},
            )
        )
        self.assertRedirects(
            response,
            reverse(
                "posts:profile", kwargs={"username": self.author.username}
            ),
        )
        self.assertEqual(Follow.objects.count(), follow_count + 1)
        self.assertEqual(
            Follow.objects.filter(user=self.user, author=self.author).exists(),
            True,
        )

    def test_unfollow_as_user(self):
        """
        Пользователь может отписываться от других пользователей
        """
        response = self.authorized_client.post(
            reverse(
                "posts:profile_follow",
                kwargs={"username": self.author.username},
            )
        )
        follow_count = Follow.objects.count()
        response = self.authorized_client.post(
            reverse(
                "posts:profile_unfollow",
                kwargs={"username": self.author.username},
            )
        )
        self.assertRedirects(
            response,
            reverse(
                "posts:profile", kwargs={"username": self.author.username}
            ),
        )
        self.assertEqual(Follow.objects.count(), follow_count - 1)
        self.assertEqual(
            Follow.objects.filter(user=self.user, author=self.author).exists(),
            False,
        )

    def test_new_post_following_author(self):
        """
        Новая запись пользователя появляется в ленте тех, кто на него подписан
        и не появляется в ленте тех, кто не подписан
        """
        Follow.objects.create(user=self.user, author=self.author)
        post = Post.objects.create(author=self.author, text="Новый пост")

        response = self.authorized_client.get(reverse("posts:follow_index"))
        self.assertIn("page_obj", response.context)
        self.assertIn(post, response.context["page_obj"])

        response = self.unfollower_client.get(reverse("posts:follow_index"))
        self.assertNotEqual(post, response.context)

    def test_no_self_follow(self):
        constraint_name = "prevent_self_follow"
        with self.assertRaisesMessage(IntegrityError, constraint_name):
            Follow.objects.create(user=self.user, author=self.user)
