# Generated by Django 3.1.2 on 2020-11-13 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0017_auto_20201111_1101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='view_count',
        ),
        migrations.AlterField(
            model_name='viewcount',
            name='viewed_post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='posts.post'),
        ),
    ]
