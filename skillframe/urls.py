from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    
    # it should be in the last
    path("__reload__/", include("django_browser_reload.urls")),
]
