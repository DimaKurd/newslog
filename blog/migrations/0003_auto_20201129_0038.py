# Generated by Django 3.1.3 on 2020-11-28 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_usernews_header'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usernews',
            old_name='owner',
            new_name='src',
        ),
    ]
