from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_user_view, name="login"),
    path("logout/", views.logout_user_view, name="logout"),
    path("register/", views.register_user_view, name="register"),
    path("user-profile/<str:pk>/", views.user_profile_view, name="user-profile"),
    path("edit-profile/", views.update_profile_view, name="edit-user-profile"),
    path("change-password/", views.change_password_view, name="change-password"),

    path('reset-password/', auth_views.PasswordResetView.as_view(template_name="registration/reset-password.html"), name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name="registration/reset-password-sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/reset-confirm.html"), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/reset-password-complete.html"), name='password_reset_complete'),
]
