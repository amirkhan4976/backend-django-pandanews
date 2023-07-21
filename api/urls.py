from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("news/topic/<str:topic>/", views.api_news_topic_view, name="api_news_topic"),
    path("news/detail/<str:pk>/<str:topic>/", views.api_news_detail_view, name="api_news_detail"),
    path("news/delete-all-refresh-news/", views.api_delete_all_refresh_view, name="api_delete-all-refresh"),

    path("user/account/info/", views.api_get_account_info),
    path("user/login/", views.api_login_user_view),
    path("user/register/", views.api_register_user_view),
    path("user/edit-profile/", views.api_update_profile_view),

    path("user/reset-password/", views.api_password_reset_sent_view, name='reset_password'),
    path("user/change-password/", views.api_change_password_view, name="change_password"),

    path("imageUploadTestView/", views.imageUploadTestView),
]
