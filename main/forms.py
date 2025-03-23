from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from main.models import UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'birth_date', 'location', 'avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and avatar.size > 2 * 1024 * 1024:  # 2MB
            raise forms.ValidationError("Розмір файлу не повинен перевищувати 2MB.")
        return avatar
#
class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password2(self):
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password1')
        if old_password == new_password:
            raise forms.ValidationError("Новий пароль повинен відрізнятися від старого.")
        return new_password