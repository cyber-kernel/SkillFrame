from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils.timezone import now

class WebhookURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def check_expired(self):
        """Deactivate webhook if expired."""
        if now() > self.expires_at and self.is_active:
            self.delete()

    def __str__(self):
        return f"Webhook {self.uuid} (Active: {self.is_active})"



class WebhookRequest(models.Model):
    webhook = models.ForeignKey(WebhookURL, on_delete=models.CASCADE, related_name="requests")
    method = models.CharField(max_length=10)
    headers = models.JSONField()
    body = models.TextField(blank=True, null=True)
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.webhook.uuid} at {self.received_at}"
