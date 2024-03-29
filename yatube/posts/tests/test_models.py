from django.test import TestCase
from posts.models import Group, Post, User


class PostModelTest(TestCase):
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
            text="С" * 20, author=cls.user, group=cls.group
        )

    def test_models_have_correct_object_names(self):
        group = self.group
        self.assertEqual(
            str(group), group.title, "У групп неправильный __str__"
        )
        post = self.post
        self.assertEqual(
            str(post), post.text[:15], "У постов неправильный __str__"
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = self.post
        field_verboses = {
            "text": "Текст поста",
            "pub_date": "Дата публикации",
            "author": "Автор",
            "group": "Группа",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value
                )

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = self.post
        field_help_texts = {
            "text": "Введите текст поста",
            "group": "Группа, к которой будет относиться пост",
        }

        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value
                )
