# Generated by Django 3.1.2 on 2020-10-20 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0007_auto_20201020_1507'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['timestamp']},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='parent_post',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='views_count',
            new_name='view_count',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='posts.comment'),
        ),
    ]
