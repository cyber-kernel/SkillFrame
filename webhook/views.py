import uuid
from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import WebhookURL, WebhookRequest
from django.contrib.auth.decorators import login_required


@login_required
def webhook_home(request):
    # Ensure the user is logged in.
    if not request.user.is_authenticated:
        return redirect("login")  # Adjust as needed.

    # Retrieve all webhooks for the current user.
    webhooks = WebhookURL.objects.filter(user=request.user)

    # Check and delete any expired webhooks.
    for wh in webhooks:
        wh.check_expired()  # This will delete the webhook if it's expired.

    # Refresh the webhooks queryset after deletion.
    webhooks = WebhookURL.objects.filter(user=request.user)

    # Get valid (non-expired and active) webhooks.
    valid_webhooks = webhooks.filter(expires_at__gt=timezone.now(), is_active=True)
    existing_webhook = valid_webhooks.first()

    if request.method == "POST":
        # Validate the expiration time input.
        try:
            expiration_time = int(
                request.POST.get("expiration_time", 60)
            )  # default: 60 minutes
        except (ValueError, TypeError):
            messages.error(request, "Invalid expiration time provided.")
            return redirect("webhook:webhook_home")

        # Only create a new webhook if no valid webhook exists.
        if not existing_webhook:
            new_webhook = WebhookURL.objects.create(
                user=request.user,
                uuid=uuid.uuid4(),
                expires_at=timezone.now() + timedelta(minutes=expiration_time),
            )
            messages.success(request, "Webhook successfully created!")
            existing_webhook = new_webhook
            # Refresh webhooks and valid_webhooks.
            webhooks = WebhookURL.objects.filter(user=request.user)
            valid_webhooks = webhooks.filter(
                expires_at__gt=timezone.now(), is_active=True
            )
        else:
            messages.info(request, "You already have a valid webhook.")

    # Recalculate valid webhooks after POST processing.
    valid_webhooks = webhooks.filter(expires_at__gt=timezone.now(), is_active=True)
    existing_webhook = valid_webhooks.first()

    # Collect all captured requests for the user's webhooks.
    captured_requests = WebhookRequest.objects.filter(webhook__in=webhooks).order_by(
        "-received_at"
    )

    return render(
        request,
        "webhook/webhook_home.html",
        {
            "webhook": existing_webhook,
            "webhooks": webhooks,
            "requests": captured_requests,
        },
    )


@csrf_exempt
def capture_webhook(request, uuid):
    """
    Capture any incoming request to the given webhook URL exactly as it is received,
    and store it in the database.
    """
    try:
        # Look up the webhook by UUID
        webhook = WebhookURL.objects.get(uuid=uuid)

        # Check if the webhook has expired
        if webhook.expires_at <= timezone.now():
            webhook.delete()
            return HttpResponse(
                "Webhook has expired and has been removed.", status=410
            )  # 410 Gone

    except WebhookURL.DoesNotExist:
        return HttpResponse("Webhook not found.", status=404)

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
    requests_qs = WebhookRequest.objects.filter(webhook__in=webhooks).order_by(
        "-received_at"
    )
    data = [
        {
            "method": req.method,
            "body": req.body,
            "headers": req.headers,
            "received_at": req.received_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for req in requests_qs
    ]
    return JsonResponse({"requests": data})
