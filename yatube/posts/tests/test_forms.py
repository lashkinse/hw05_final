import shutil
import tempfile

from http import HTTPStatus

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.forms import PostForm, CommentForm
from posts.models import Group, Post, User, Comment

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostForm()
        cls.user = User.objects.create_user(username="user")
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )
        cls.image = SimpleUploadedFile(
            name="small.gif", content=small_gif, content_type="image/gif"
        )
        cls.post = Post.objects.create(text="Тестовый пост", author=cls.user)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post_as_user(self):
        """
        При отправке валидной формы создаётся новая запись в базе данных
        """
        posts_count = Post.objects.count()
        form_data = {
            "text": "Новый пост",
            "image": self.image,
        }
        response = self.authorized_client.post(
            reverse("posts:create_post"), data=form_data, follow=True
        )
        self.assertRedirects(
            response,
            reverse("posts:profile", kwargs={"username": self.user.username}),
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)

        post = Post.objects.first()
        self.assertEqual(post.text, "Новый пост")
        self.assertEqual(post.image, "posts/small.gif")

    def test_post_edit_as_user(self):
        """
        При редактировании существующего поста изменяется
        соответствующая ему запись в базе данных
        """
        form_data = {
            "text": "Измененный пост",
        }
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
                text="Измененный пост",
                id=self.post.id,
            ).exists()
        )

    def test_post_create_as_guest(self):
        """
        Проверка анонимных клиентов на возможность создания новых записей
        """
        posts_count = Post.objects.count()
        form_data = {"text": self.post.text}
        response = self.guest_client.post(
            reverse("posts:create_post"), data=form_data, follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class CommentFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="user")
        cls.post = Post.objects.create(text="Тестовый пост", author=cls.user)
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text="Комментарий",
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_add_comment_as_user(self):
        """
        При отправке валидной формы создаётся новая запись в базе данных
        """
        comments_count = Comment.objects.count()
        form_data = {
            "text": "Новый комментарий",
        }
        response = self.authorized_client.post(
            reverse("posts:add_comment", kwargs={"post_id": self.post.id}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("posts:post_detail", kwargs={"post_id": self.post.id}),
        )
        self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertTrue(
            Comment.objects.filter(
                text="Новый комментарий",
            ).exists()
        )

    def test_add_comment_as_guest(self):
        """
        Проверка анонимных клиентов на возможность добавления комментариев
        """
        comments_count = Comment.objects.count()
        form_data = {
            "text": "Новый комментарий",
        }
        response = self.guest_client.post(
            reverse("posts:add_comment", kwargs={"post_id": self.post.id}),
            data=form_data,
            follow=True,
        )
        self.assertEqual(Comment.objects.count(), comments_count)
        self.assertFalse(
            Comment.objects.filter(
                text="Новый комментарий",
            ).exists()
        )
