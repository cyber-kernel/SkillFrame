import uuid
from datetime import timedelta
from django.utils.timezone import now
from django.shortcuts import render
from django.contrib import messages  # Import the messages framework
from .models import WebhookURL

def webhook_home(request):
    webhook = None
    webhooks = WebhookURL.objects.filter(user=request.user)  # Fetch all webhooks for the logged-in user

    # Check if there is an existing valid webhook
    existing_webhook = webhooks.filter(expires_at__gt=now()).first()  # Get the first non-expired webhook if exists

    if request.method == "POST":
        # Only create a new webhook if there's no valid existing one
        if not existing_webhook:
            expiration_time = int(request.POST.get("expiration_time", 60))  # Default 60 minutes
            webhook = WebhookURL.objects.create(
                user=request.user,
                uuid=uuid.uuid4(),
                expires_at=now() + timedelta(minutes=expiration_time)
            )
            # Set success message when a new webhook is created
            messages.success(request, "Webhook successfully created!")
            # Fetch updated webhooks after creating a new one
            webhooks = WebhookURL.objects.filter(user=request.user)
        else:
            # Set info message when a valid webhook already exists
            messages.info(request, "You already have a valid webhook.")

    # If an existing valid webhook exists, use it
    if existing_webhook:
        webhook = existing_webhook

    return render(request, "webhook/webhook_home.html", {"webhook": webhook, "webhooks": webhooks})
