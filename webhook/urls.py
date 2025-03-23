from django.urls import path
from . import views

app_name = "webhook"

urlpatterns = [
    path("", views.webhook_home, name="webhook_home"),
    path("<uuid:uuid>/", views.capture_webhook, name="capture_webhook"),
    path("get_requests_json/", views.get_requests_json, name="get_requests_json"),
]
