from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    category_image = models.ImageField(
        upload_to="category_images/", null=True, blank=True
    )
    slug = models.SlugField(max_length=30, unique=True)
    description = models.TextField(max_length=150, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Use the correct slugify function
        super().save(*args, **kwargs)  # Always call the parent save method

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    content = models.TextField()
    thumbnail = models.ImageField(
        upload_to="thumbnails/Y/%m/%d/", null=True, blank=True
    )
    views = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    published_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="posts", null=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.comment


class CommentReply(models.Model):
    reply = models.TextField()
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies", null=True, blank=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="replies", blank=True, null=True
    )
    published_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.reply
