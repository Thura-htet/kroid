# Generated by Django 3.1.2 on 2020-11-06 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_post_author_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='argument_count',
            new_name='comment_count',
        ),
    ]