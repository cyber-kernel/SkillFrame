from django.shortcuts import render
from django.utils.html import escape

# Create your views here.
def main(request):
    return render(request, "todo/main.html")

def todo(request):
    if request.method == "POST":
        data = request.POST
        title = escape(data.get("todoTitle", '').strip())
        desc = escape(data.get("todoDescription", '').strip())
        priority = escape(data.get("todoPriority", '').strip())
        
    return render(request, "todo/todo.html")