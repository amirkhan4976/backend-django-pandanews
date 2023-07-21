from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage_view, name="home"),
    path("news-detail/<str:pk>/<str:topic>/", views.news_detail_view, name="news-detail"),
    path("news-topic/<str:topic>/", views.news_topic, name="news-topic"),
    path("delete-all-refresh-news/", views.delete_all_refresh_news, name="delete-all-refresh-news"),
]
