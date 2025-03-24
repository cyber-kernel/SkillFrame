from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import Category, Post, Comment, CommentReply


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")


admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "slug", "category")
    # Override the widget for TextField (which includes HTMLField) to use TinyMCE
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE(attrs={"cols": 80, "rows": 30})},
    }


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "comment", "created_on")


admin.site.register(Comment, CommentAdmin)


class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ("comment", "author", "reply", "published_on")


admin.site.register(CommentReply, CommentReplyAdmin)
