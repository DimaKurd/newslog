# Generated by Django 3.1.3 on 2020-11-30 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20201130_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernews',
            name='picture',
            field=models.ImageField(null=True, upload_to='userpic/'),
        ),
    ]
