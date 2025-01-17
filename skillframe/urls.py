from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('todo/', include('todo.urls')),
    path('', views.index, name="index"),
    path('about_me/', views.about_me, name="about_me"),
    # it should be in the last
    path("__reload__/", include("django_browser_reload.urls")),
]
