# Generated by Django 2.2.16 on 2022-10-31 08:17

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_comment_follow'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={
                'ordering': ('-created',),
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.AlterModelOptions(
            name='follow',
            options={
                'ordering': ('-created',),
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.AddField(
            model_name='follow',
            name='created',
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name='Дата создания',
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='created',
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name='Дата создания',
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comments',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Автор',
            ),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(
                auto_now_add=True, verbose_name='Дата создания'
            ),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comments',
                to='posts.Post',
                verbose_name='Пост',
            ),
        ),
        migrations.AlterField(
            model_name='follow',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='following',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Автор',
            ),
        ),
        migrations.AlterField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='follower',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Подписчик',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(
                blank=True,
                help_text='Добавить картинку',
                upload_to='posts/',
                verbose_name='Картинка',
            ),
        ),
    ]