from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,re_path
from . import views
from .views import ProfileUser


urlpatterns = [
    path('profile/<str:username>/', ProfileUser.as_view(), name ='profile')
]

