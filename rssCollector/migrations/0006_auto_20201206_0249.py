# Generated by Django 3.1.3 on 2020-12-05 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rssCollector', '0005_auto_20201206_0244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newssrc',
            name='descr',
            field=models.TextField(null=True),
        ),
    ]