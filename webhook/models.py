from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

class WebhookURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def check_expired(self):
        """deactivate webhook if expired"""
        if now() > self.expires_at:
            self.is_active = False
            self.save()

    def __str__(self):
        return f"Webhook {self.uuid} (Active: {self.is_active})"