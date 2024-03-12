from datetime import datetime

from braces.views import GroupRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest,
                         HttpResponseNotFound, Http404)
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView, FormView

from .forms import UserForm, ContactForm, LoginForm, SignUpForm, CommentForm, SearchForm, NewsUpdateForm, NewsCreateForm
from .models import News, Category, Comment
# Create your views here.
from django.views import View
from django.contrib.auth.decorators import permission_required, login_required


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = 'contact/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'registration/login.html',{'form':form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username, password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('/')
        if form.errors:
            messages.error(request, 'Your username and password didn\'t match. Please try again')
        return render(request, 'registration/login.html', {'form': form})


class MainLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('HomePage')

    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

def sign_out(request):
    logout(request)
    messages.success(request,'You have been logged out')
    return redirect('login')


#Registaration
def registration(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'registration/registration.html', { 'form': form})

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request,'Вы успешно зарегистрировались')
            return redirect('/')
        else:
            return render(request,'registration/registration.html',{'form':form})


## CRUD
class NewView(ListView):
    template_name = "new_view.html"
    model = News
    context_object_name = "new_list"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['News'] = News.objects.select_related('category')
        return context

def create_news():
    if Category.objects.all().count() == 0:
        Category.objects.create(category="Sport")
        Category.objects.create(category="Gaming")
        Category.objects.create(category="War")


class NewsGet(LoginRequiredMixin,ListView):
    model = News
    context_object_name = "news_list"

    def get_queryset(self):
        return News.objects.filter(author=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['Neews'] = self.get_queryset()
        return context


class NewsCategory(ListView):
    model = News
    template_name = 'NewsCategory.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        category = Category.objects.filter(slug=self.kwargs['slug'])
        return News.objects.filter(category__in=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        return context

class AllCategoriesView(ListView):
    model = Category
    template_name = 'all_categories.html'
    context_object_name = 'categories'


# class NewsCategory(ListView):
#     template_name = 'news/NewsCategory.html'
#     context_object_name = 'news_category'
#     allow_empty = False
#
#     def get_queryset(self):
#         queryset = News.objects.filter(category__slug=self.kwargs['slug'])
#         if not queryset.exists():
#             raise Http404("No posts found in this category.")
#         return queryset
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = Category.objects.get(slug=self.kwargs['slug'])
#         return context

class SearchResultsView(ListView):
    model = News
    form_class = SearchForm
    context_object_name = 'news_title'
    template_name = 'news/search.html'

    def get_queryset(self): # новый
        query = self.request.GET.get('title')
        object_list = News.objects.filter(
            Q(title__icontains=query)
        )
        return object_list


    # def get_queryset(self):
    #     return News.objects.filter(title__icontains=self.request.GET.get('s'))
    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['s'] = f"s={self.request.GET.get('s')}&"
    #     return context




class NewsCreate(CreateView): # GroupRequiredMixin для групп
    create_news()
    model = News
    form_class = NewsCreateForm


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        self.request.user.save()
        return HttpResponseRedirect('/')

    # def add_news(request):
    #     if not request.user.has_perm('news.add_news'):
    #         raise PermissionDenied


# class RedirectPermissionRequiredMixin(PermissionRequiredMixin,):
#     login_url = reverse_lazy('UpdateView')
#
#     def handle_no_permission(self):
#         return redirect(self.get_login_url())

# RedirectPermissionRequiredMixin,
class UpdateNews(UpdateView):
    form_class = NewsUpdateForm
    model = News
    template_name = 'news/news_update.html'
    success_url = '/'




class DeleteNews(DeleteView):
    model = News
    success_url = '/'
    context_object_name = "item"

    def add_news(request):
        if not request.user.has_perm('news.delete_news'):
            raise PermissionDenied

# RedirectPermissionRequiredMixin,

class NewsDetail( DetailView):
    # permission_required = 'news.view_news'
    model = News
    context_object_name = 'new'
    template_name = 'news/news_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context ["category"]  = "Life"
        context ['categories'] = Category.objects.all()
        context ['existing_comments'] = Comment.objects.order_by('-created')
        context ['comment_form'] = CommentForm()
        return context


    def post (self, request, pk, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            if request.user.is_authenticated:
                comment = comment_form.save(commit=False)
                comment.name = request.user.username
                news = self.get_object()
                comment.news = news
                comment.user = request.user
                comment.save()
                return HttpResponseRedirect(reverse_lazy('NewsDetail', kwargs={'pk': pk}))
        else:
            return render (request, 'news/news_detail',context={'comment_form':comment_form,'object': self.get_object()})




## CRUD

