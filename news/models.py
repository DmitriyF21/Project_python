import uuid
from datetime import  datetime

from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _




class Category(models.Model):
    category = models.CharField(max_length=30)
    slug = models.SlugField(null=True, verbose_name='category_link', default=uuid.uuid1)

    def __str__(self):
        return self.category
    class Meta:
        verbose_name_plural="categories"
        app_label = 'news'

    def get_absolute_url(self):
        return reverse('category',kwargs={'slug':self.slug})


class News(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=10000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="img/", blank=True)
    slug = models.SlugField(null=True,verbose_name='Link',default=uuid.uuid1)

    class Meta:
        verbose_name_plural = "news"
        app_label = 'news'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title






class Comment (models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE,related_name='comments')
    comment = models.TextField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['created']


    def __str__(self): # repr для консольного отображения, а str для print
        return self.comment
