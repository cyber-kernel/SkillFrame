from django.urls import path
from . import views

app_name = "webhook"

urlpatterns = [
    path("", views.webhook_home, name="webhook_home"),
]