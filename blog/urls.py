from django.urls import path
from .import views

app_name = "blog"

urlpatterns = [
    path("all_blogs/", views.all_blogs, name="all_blogs"),
    path("<slug:slug>/", views.view_post, name="view_post"),
]