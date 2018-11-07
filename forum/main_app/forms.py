from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ForumUser, Thread, Post


class ForumUserCreationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = ForumUser
        fields = ("username", "gender", "password1", "password2")

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Логин'
                    }
                ),
            'gender': forms.Select(
                attrs={
                    'class': 'form-control',
                    }
                )
            }


class ThreadCreateForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ("title", "description", "image")

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Название темы'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Текст темы'
                }
            ),
        }


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "description")

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'reply-post form-control',
                    'placeholder': 'Заголовок ответа'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Текст ответа'
                }
            ),
        }


class ForumUserUpdateForm(forms.Form):
    email = forms.EmailField(required=False, label='Электронная почта')
    first_name = forms.CharField(required=False, label='Имя')
    last_name = forms.CharField(required=False, label='Фамилия')
    city = forms.CharField(required=False, label='Город')
    avatar = forms.ImageField(required=False, label='Аватар')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ForumUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control', 'value': self.request.user.email})
        self.fields['first_name'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': self.request.user.first_name})
        self.fields['last_name'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': self.request.user.last_name})
        self.fields['city'].widget = forms.TextInput(attrs={'class': 'form-control', 'value': ForumUser.objects.get(username=self.request.user).city})
        self.fields['avatar'].widget = forms.FileInput(attrs={'id': 'file-input' })
