# Generated by Django 3.1.3 on 2020-12-05 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rssCollector', '0004_newssrc_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newssrc',
            name='descr',
            field=models.TextField(blank=True, null=True),
        ),
    ]