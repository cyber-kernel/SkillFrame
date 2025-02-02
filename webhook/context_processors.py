# yourapp/context_processors.py

from django.conf import settings

def domain_name(request):
    # Use request.get_host() for dynamic domain or fetch from settings
    return {
        'domain_name': settings.DOMAIN_NAME or request.get_host()
    }
