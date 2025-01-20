from django.shortcuts import redirect, render
from django.db.models import F
from .models import Post
from django.contrib import messages
# Create your views here.
def all_blogs(request):
    all_posts = Post.objects.filter(is_active=True, is_published=True).order_by("-published_on")    
    return render(request, "blog/all_blogs.html", {"all_posts": all_posts})

def view_post(request, slug):
    post = Post.objects.filter(is_active=True, is_published=True, slug=slug).annotate(
        updated_views=F('views') + 1
    ).first()

    if not post:
        messages.error(request, "Post not found")
        return redirect("blog:all_blogs")

    post.views = post.updated_views
    post.save()

    category_posts = Post.objects.filter(is_active=True, is_published=True, category=post.category).exclude(slug=slug)[:3]
    ctx = {
        "post": post,
        "category_posts": category_posts
    }
    return render(request, "blog/view_post.html", ctx)



