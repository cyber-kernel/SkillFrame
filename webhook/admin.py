from django.contrib import admin
from .models import WebhookURL

# Register your models here.
class WebhookURLAdmin(admin.ModelAdmin):
    list_display = ('user', 'uuid', 'created_at', 'expires_at', 'is_active')
admin.site.register(WebhookURL)