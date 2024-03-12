from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from .models import News, Category, Comment


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category']
    search_fields = ("category", )


class NewsForm(forms.ModelForm):
    model = News
    fields = "__all__"

    def clean_title(self):
        if self.cleaned_data['title'] == 'Fake':
            raise forms.ValidationError('No fake news')

        return self.cleaned_data['title']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsForm
    list_display = ['title','description','get_img']
    prepopulated_fields = {"slug": ('title',)}
    search_fields = ("title", )


    def get_img(self,obj):
        if obj.image:
            return mark_safe(f'<image src="{obj.image.url}" width="50">')
        return '-'
    get_img.short_description = 'picture'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment']


admin.site.unregister(User)


@admin.register(User)
class CustomAdminUser(UserAdmin):
    readonly_fields = [
        'date_joined',
    ]
    def get_form(self,request,obj = None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['username'].disabled = True

        return form







