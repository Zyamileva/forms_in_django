from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import ImageField

from main.models import UserProfile


class RegistrationForm(UserCreationForm):
    """
    A form for user registration, inheriting from Django's UserCreationForm.

    Adds an email field and validation for unique usernames and emails.
    """

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self) -> str:
        """
        Validates that the entered username is unique.

        Raises:
            ValidationError: If the username already exists.

        Returns:
            str: The cleaned username.
        """
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self) -> str:
        """
        Validates that the entered email is unique.

        Raises:
            ValidationError: If the email already exists.

        Returns:
            str: The cleaned email.
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email


class UserProfileForm(forms.ModelForm):
    """
    A form for updating user profiles, based on the UserProfile model.

    Includes validation to limit the avatar file size to 2 MB.
    """

    class Meta:
        model = UserProfile
        fields = ["bio", "birth_date", "location", "avatar"]

    def clean_avatar(self) -> ImageField:
        """
        Validates the size of the uploaded avatar.

        Raises:
            ValidationError: If the avatar file size exceeds 2 MB.

        Returns:
            avatar: The cleaned avatar.
        """
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            MAX_SIZE = 2 * 1024 * 1024  # 2 MB
            if avatar.size > MAX_SIZE:
                raise forms.ValidationError("Файл повинен бути меншим за 2 МБ.")
        return avatar


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Validates that the new password is different from the old password.

    Raises:
        ValidationError: If the new password matches the old password.

    Returns:
        str: The confirmed new password.
    """

    def clean_new_password2(self) -> str:
        """
        Validates that the new password is different from the old password.

        Raises:
            ValidationError: If the new password matches the old password.

        Returns:
            str: The confirmed new password.
        """
        old_password = self.cleaned_data.get("old_password")
        new_password = self.cleaned_data.get("new_password1")
        if old_password == new_password:
            raise forms.ValidationError(
                "Новий пароль повинен відрізнятися від старого."
            )
        return new_password
