# Generated by Django 5.0.1 on 2024-02-16 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_alter_comment_news_alter_news_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, default='forest.jpg', upload_to='img/'),
        ),
    ]
