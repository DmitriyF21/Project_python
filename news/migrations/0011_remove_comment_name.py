# Generated by Django 5.0.1 on 2024-02-16 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_news_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='name',
        ),
    ]