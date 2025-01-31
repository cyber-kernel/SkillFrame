from django.shortcuts import render

# Create your views here.

def webhook_home(request):
    return render(request, "webhook/webhook_home.html")