from django.test import TestCase
from django.urls import reverse

from homework_07.first_project.news.models import Category, News


class NewsTestCase(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(category="TestCategory1")
        self.category2 = Category.objects.create(category="TestCategory2")
        self.news1 = News.objects.create(title="TestNews1", description="TestDescription1", category=self.category1)
        self.news2 = News.objects.create(title="TestNews2", description="TestDescription2", category=self.category2)

    def tearDown(self):
        self.category1.delete()
        self.category2.delete()
        self.news1.delete()
        self.news2.delete()

    def test_news_view_context(self):
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['News_list']), 2)
