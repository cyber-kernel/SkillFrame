from django.contrib import admin
from .models import Category, Post, Comment, CommentReply

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ('name', 'slug') 
admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ('title', 'slug', 'category')

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'comment', 'created_on')

admin.site.register(Comment, CommentAdmin)

class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ('comment', 'author', 'reply', 'published_on')

admin.site.register(CommentReply, CommentReplyAdmin)