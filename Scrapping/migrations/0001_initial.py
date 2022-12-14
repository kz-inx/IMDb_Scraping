# Generated by Django 4.1 on 2022-08-05 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IMDbScrapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('link', models.CharField(max_length=1000)),
                ('rating', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('year', models.CharField(max_length=200)),
                ('runtime', models.CharField(max_length=100)),
                ('categories', models.CharField(max_length=300)),
                ('vote', models.CharField(max_length=300)),
            ],
        ),
    ]
