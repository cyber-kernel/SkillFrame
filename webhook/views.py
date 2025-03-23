import uuid
from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import WebhookURL, WebhookRequest
from django.contrib.auth.decorators import login_required


def webhook_home(request):
    # Ensure the user is logged in.
    if not request.user.is_authenticated:
        return redirect("login")  # Adjust as needed based on your authentication flow.

    webhook = None
    webhooks = WebhookURL.objects.filter(user=request.user)
    # Get the first valid, active webhook (non-expired).
    existing_webhook = webhooks.filter(
        expires_at__gt=timezone.now(), is_active=True
    ).first()

    if request.method == "POST":
        # Validate the expiration time input.
        try:
            expiration_time = int(
                request.POST.get("expiration_time", 60)
            )  # default: 60 minutes
        except (ValueError, TypeError):
            messages.error(request, "Invalid expiration time provided.")
            return redirect("webhook:webhook_home")

        # Only create a new webhook if there's no valid one.
        if not existing_webhook:
            new_webhook = WebhookURL.objects.create(
                user=request.user,
                uuid=uuid.uuid4(),
                expires_at=timezone.now() + timedelta(minutes=expiration_time),
            )
            messages.success(request, "Webhook successfully created!")
            webhook = new_webhook
            # Refresh list of webhooks.
            webhooks = WebhookURL.objects.filter(user=request.user)
        else:
            messages.info(request, "You already have a valid webhook.")
            webhook = existing_webhook

    # Check and update expiration status if needed.
    if existing_webhook:
        existing_webhook.check_expired()
        if not existing_webhook.is_active:
            webhook = None

    # Collect all captured requests for the logged-in user's webhooks.
    captured_requests = WebhookRequest.objects.filter(webhook__in=webhooks).order_by(
        "-received_at"
    )

    return render(
        request,
        "webhook/webhook_home.html",
        {"webhook": webhook, "webhooks": webhooks, "requests": captured_requests},
    )


@csrf_exempt
def capture_webhook(request, uuid):
    """
    Capture any incoming request to the given webhook URL exactly as it is received,
    and store it in the database.
    """
    try:
        # Look up the webhook by UUID and ensure it's active and not expired.
        webhook = WebhookURL.objects.get(
            uuid=uuid, expires_at__gt=timezone.now(), is_active=True
        )
    except WebhookURL.DoesNotExist:
        return HttpResponse("Webhook not found or expired.", status=404)

    # Attempt to decode the raw request body.
    try:
        raw_body = request.body.decode("utf-8")
    except Exception:
        raw_body = ""

    # Build a raw request string that captures the entire request as received.
    raw_request = f"{request.method} {request.build_absolute_uri()} HTTP/1.1\n"
    for header, value in request.headers.items():
        raw_request += f"{header}: {value}\n"
    raw_request += "\n" + raw_body

    # Save the incoming request details with the complete raw request in the 'body' field.
    WebhookRequest.objects.create(
        webhook=webhook,
        method=request.method,
        headers=dict(request.headers),
        body=raw_request,
    )

    return JsonResponse({"message": "Request captured successfully."})



@login_required
def get_requests_json(request):
    # Get all webhooks for the logged-in user.
    webhooks = WebhookURL.objects.filter(user=request.user)
    # Fetch all requests for those webhooks, ordered by received time (most recent first)
    requests_qs = WebhookRequest.objects.filter(webhook__in=webhooks).order_by('-received_at')
    data = [{
        "method": req.method,
        "body": req.body,
        "headers": req.headers,
        "received_at": req.received_at.strftime("%Y-%m-%d %H:%M:%S")
    } for req in requests_qs]
    return JsonResponse({"requests": data})