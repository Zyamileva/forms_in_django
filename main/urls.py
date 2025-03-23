from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('register/', views.register_view, name='register_view'),
    path('profile/', views.profile_view, name='profile_view'),
    # path('profile/<int:user_id>/', views.profile_view, name='profile_view'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile_view'),
    path('change-password/', views.change_password_view, name='change_password_view'),
]