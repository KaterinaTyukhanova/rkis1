from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import AdvUser, Question


class AdvUserForm(forms.ModelForm):
    last_name = forms.CharField(widget=forms.TextInput, label='Фамилия')
    first_name = forms.CharField(widget=forms.TextInput, label='Имя')
    username = forms.CharField(label='Логин', widget=forms.TextInput)
    email = forms.EmailField(label='Email', widget=forms.EmailInput)

    class Meta:
        model = AdvUser
        fields = ("last_name", "first_name", "username", "email", "avatar")


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ("question_image",)


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput, required=True)
    email = forms.EmailField(label='Email', widget=forms.EmailInput, required=True)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput, required=True)

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2')
