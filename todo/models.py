from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Todo(models.Model):
    PRIORITY = (
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")
    title = models.CharField(max_length=30, default="title here")
    desc = models. CharField(max_length=100, default="descriptin here")
    priority = models.CharField(max_length=6, choices=PRIORITY, default=PRIORITY[1][1])
    created_on = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.title} - {self.get_priority_display()}" 