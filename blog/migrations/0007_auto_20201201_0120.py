# Generated by Django 3.1.3 on 2020-11-30 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20201130_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernews',
            name='picture',
            field=models.ImageField(max_length=1024, null=True, upload_to='userpic/'),
        ),
    ]
