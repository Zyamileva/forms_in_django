from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, update_session_auth_hash
from .forms import RegistrationForm, UserProfileForm, CustomPasswordChangeForm
from main.models import UserProfile


def home(request: HttpRequest) -> HttpResponse:
    """
    Renders the home page.

    Returns the base template.
    """
    return render(request, "main/base.html")


def _extracted_from_register_view_5(form, request: HttpRequest) -> HttpResponse:
    """
    Saves user data, creates a user profile, logs in the user, and redirects to the profile view.

    Handles user creation and login after form validation.
    """
    user = form.save(commit=False)
    user.set_password(form.cleaned_data["password1"])
    user.save()
    UserProfile.objects.create(user=user)
    login(request, user)
    return redirect("profile_view")


def register_view(request: HttpRequest) -> HttpResponse:
    """
    Handles user registration.

    Processes the registration form, creates a new user, and redirects to the profile page upon successful registration.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return _extracted_from_register_view_5(form, request)
    else:
        form = RegistrationForm()
    return render(request, "main/register_form.html", {"form": form})


@login_required
def profile_view(request: HttpRequest, username=None) -> HttpResponse:
    """
    Displays a user's profile.

    Retrieves and displays the profile information for the specified user, or the current user if no username is provided.
    """
    user = get_object_or_404(User, username=username) if username else request.user
    profile = get_object_or_404(UserProfile, user=user)
    return render(request, "main/profile.html", {"profile": profile})


@login_required
def edit_profile_view(request: HttpRequest) -> HttpResponse:
    """
    Allows users to change their password.

    Handles password change form submission and updates the user's session.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("home")
    else:
        form = UserProfileForm(instance=profile)
    return render(request, "main/edit_profile.html", {"form": form})


@login_required
def change_password_view(request: HttpRequest) -> HttpResponse:
    """
    Allows users to change their password.

    Handles password change form submission and updates the user's session.
    """
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password changed successfully.")
            return redirect("profile_view")
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, "main/change_password.html", {"form": form})
