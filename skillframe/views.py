from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, "index.html")

def about_me(request):
    return render(request, "about_me.html")
def contact_me(request):
    return render(request, "contact_me.html")