from django.contrib import admin
from .models import Todo
# Register your models here.

class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'priority', 'created_on')

admin.site.register(Todo, TodoAdmin)

