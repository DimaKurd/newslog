# Generated by Django 3.1.3 on 2020-12-01 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rssCollector', '0003_auto_20201129_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='newssrc',
            name='icon',
            field=models.URLField(default=''),
        ),
    ]
