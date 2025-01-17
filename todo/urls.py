from django.urls import path
from . import views
app_name = "todo"
urlpatterns = [
    path("", views.main, name="main"),
    path("addtodo/", views.addtodo, name="todo"),
]