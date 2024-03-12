from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import FormView

from .models import News, Comment
from django.forms import ModelForm


class UserForm(forms.Form):
    name = forms.CharField(label="Имя",help_text="Введите свое имя")
    age = forms.IntegerField(label="Возраст")
    comment = forms.CharField(label="Комментарий", widget=forms.Textarea)


class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'description', 'category', 'image')
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'category': 'Категория',
            'image': 'Изображение',
        }


class NewsUpdateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'description', 'category', 'image')
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'category': 'Категория',
            'image': 'Изображение',
        }

class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField()

    def send_email(self):
        pass


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'category')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65, label='Логин')
    password = forms.CharField(max_length=65, widget=forms.PasswordInput, label='Пароль')


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'username', 'password1','password2' ]
        # labels = {
        #     'email': 'Электронная почта',
        #     'first_name': 'Имя',
        #     'username': 'Имя пользователя',
        #     'password': 'Пароль',
        # }


class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields = ['comment']


class SearchForm(forms.Form):
    title = forms.CharField(max_length=200)

