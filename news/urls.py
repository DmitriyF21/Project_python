from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,re_path
from django.views.generic import TemplateView, UpdateView

from . import views
from .views import NewView, NewsDetail, NewsGet, UpdateNews, \
    DeleteNews, NewsCreate, ContactView, sign_in, MainLoginView, SearchResultsView, NewsCategory, AllCategoriesView

urlpatterns = [
   # path("", NewView.as_view(template_name="home.html"), name="HomePage"),
    path("", NewView.as_view(template_name="new_view.html"), name="HomePage"),
    path('category/<slug:slug>/', NewsCategory.as_view(template_name="NewsCategory.html"), name='news_category'),
    path('categories/', AllCategoriesView.as_view(template_name="all_categories.html"), name='all_categories'),
    path("search/", SearchResultsView.as_view(), name="search"),
    path("registration/", views.registration, name="registration"),
    path("contact/", ContactView.as_view(), name="Contact"),
    path("login/", MainLoginView.as_view(), name = "login"),
    path("logout/", views.sign_out, name ='logout'),
    path("create/", NewsCreate.as_view(), name="NewsCreate"),
    path("get/", NewsGet.as_view(), name="NewsGet"),
    path("get/<int:pk>", NewsDetail.as_view(), name="NewsDetail"),
    path("update/<int:pk>", UpdateNews.as_view(), name="UpdateView"),
    path("delete/<int:pk>", DeleteNews.as_view(), name="DeleteProduct"),

]


# path('category/<str:slug>/', NewsCategory.as_view(template_name="home.html"), name='category_news'),