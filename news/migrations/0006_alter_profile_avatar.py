# Generated by Django 5.0.1 on 2024-02-11 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_news_options_alter_news_image_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='avatar.jpg', upload_to='profile_pics'),
        ),
    ]
