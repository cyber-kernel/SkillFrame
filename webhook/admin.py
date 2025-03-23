from django.contrib import admin
from .models import WebhookURL, WebhookRequest

# Register your models here.
class WebhookURLAdmin(admin.ModelAdmin):
    list_display = ('user', 'uuid', 'created_at', 'expires_at', 'is_active')
admin.site.register(WebhookURL)

class WebhookRequestAdmin(admin.ModelAdmin):
    list_display = ('webhook', 'method', 'received_at')
admin.site.register(WebhookRequest)