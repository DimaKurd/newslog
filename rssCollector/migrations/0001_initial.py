# Generated by Django 3.1.3 on 2020-11-23 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsSrc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('link', models.URLField()),
                ('descr', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='WebNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(default='')),
                ('picture', models.URLField(null=True)),
                ('date', models.DateTimeField()),
                ('link', models.TextField(default='')),
                ('src', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rssCollector.newssrc')),
            ],
        ),
        migrations.AddField(
            model_name='newssrc',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rssCollector.type'),
        ),
    ]
