from django.urls import path
from django.views.decorators.cache import cache_page 
from . import views

urlpatterns = [
    path("", views.HomeNews.as_view(), name="index"),
    path("news/add-news/", views.addNews, name="addNews"),
    path(
        "category/<int:category_id>/", views.GetCategory.as_view(), name="getCategory"
    ),
    path("news/<int:news_id>/", views.viewDetail, name="getNews"),
]
