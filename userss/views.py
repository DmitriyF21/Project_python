from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView, UpdateView

from .models import Profile
from .forms import ProfileForm


# Create your views here.


class ProfileUser(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'userss/profile.html'
    success_url = '/'

    def get_object(self):
        return self.request.user
