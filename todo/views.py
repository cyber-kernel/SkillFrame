from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import escape
from .models import Todo
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

MAX_TITLE_SIZE = 100
MAX_DEVCODE_SIZE = 200
VALID_PRIORITIES = ["low", "medium", "high"]


def main(request):
    return render(request, "todo/main.html")


@login_required
def addtodo(request):
    todos = Todo.objects.filter(user=request.user)
    if request.method == "POST":
        data = request.POST
        title = escape(data.get("todoTitle", "").strip())
        desc = escape(data.get("todoDescription", "").strip())
        priority = escape(data.get("todoPriority", "").strip())

        if priority not in VALID_PRIORITIES:
            messages.error(request, "Invalid priority")
            return redirect("todo:todo")

        if len(title) > MAX_TITLE_SIZE:
            messages.error(request, "Title too long")
            return redirect("todo:todo")

        if len(desc) > MAX_DEVCODE_SIZE:
            messages.error(request, "Description is too long")
            return redirect("todo:todo")

        try:
            Todo.objects.create(
                user=request.user, title=title, desc=desc, priority=priority
            )
            messages.success(request, "Todo created successfully")
            return redirect("todo:todo")
        except Exception as e:
            messages.error(request, f"Error creating todo Try Again: {e}")
            return redirect("todo:todo")

    return render(request, "todo/todo.html", {"todos": todos})


def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    messages.success(request, "Task Deleted successfully!")
    return redirect("todo:todo")


def edit_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)  # Use `id` instead of `todo_id`

    if request.method == "POST":
        data = request.POST
        title = escape(data.get("todoTitle", "").strip())
        desc = escape(data.get("todoDescription", "").strip())
        priority = escape(data.get("todoPriority", "").strip())

        if priority not in VALID_PRIORITIES:
            messages.error(request, "Invalid priority")
            return redirect("todo:todo")

        if len(title) > MAX_TITLE_SIZE:
            messages.error(request, "Title too long")
            return redirect("todo:todo")

        if len(desc) > MAX_DEVCODE_SIZE:
            messages.error(request, "Description is too long")
            return redirect("todo:todo")

        try:
            todo.title = title  # Use the actual `todo` instance
            todo.desc = desc
            todo.priority = priority
            todo.save()  # Save the changes to the database
            messages.success(request, "Task Edited Succesfully!")
            return redirect("todo:todo")
        except Exception:
            messages.error(request, "Error in Editieng todo. Try Again.")
            return redirect("todo:todo")

    return render(request, "todo/todo.html", {"todo": todo})


def mark_done(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.is_done = True
    todo.save()
    return redirect("todo:todo")