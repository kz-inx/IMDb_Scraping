# Generated by Django 4.1 on 2022-08-24 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Scrapping', '0004_alter_imdbscrapping_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='imdbscrapping',
            name='image_file',
            field=models.ImageField(null=True, upload_to='images'),
        ),
        migrations.AddField(
            model_name='imdbscrapping',
            name='image_urls',
            field=models.URLField(default=None, null=True),
        ),
    ]
