from django.urls import path
from . import views
app_name = "todo"
urlpatterns = [
    path("", views.main, name="main"),
    path("addtodo/", views.addtodo, name="todo"),
    path("delete/<int:todo_id>/", views.delete_todo, name="delete_todo"),
    path("edit/<int:todo_id>/", views.edit_todo, name="edit_todo"),
    path("mark-done/<int:todo_id>/", views.mark_done, name="mark_done"),
]