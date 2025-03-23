from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """
    Extends the built-in User model to store additional user profile information.

    Includes fields for biography, birth date, location, and an avatar image.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return self.user.username
