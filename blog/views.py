from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db.models import F, Count
from .models import Post, Comment, CommentReply, Category
from django.contrib.auth.decorators import login_required


def all_blogs(request):
    all_posts = Post.objects.filter(is_active=True, is_published=True).order_by(
        "published_on"
    )
    return render(request, "blog/all_blogs.html", {"all_posts": all_posts})


def handle_comments(post):
    """Fetch active comments and their replies for a blog post."""
    comments = post.comments.filter(is_active=True)
    comment_replies = CommentReply.objects.filter(is_active=True)
    comments_with_replies = [
        {"comment": comment, "replies": comment_replies.filter(comment=comment)}
        for comment in comments
    ]
    return comments_with_replies


def view_post(request, slug):
    """Handles blog post view and interactions."""
    post = (
        Post.objects.filter(is_active=True, is_published=True, slug=slug)
        .annotate(updated_views=F("views") + 1)
        .first()
    )

    if not post:
        messages.error(request, "Post not found")
        return redirect("blog:all_blogs")

    # Update the view count
    post.views = post.updated_views
    post.save()

    # If a comment is submitted, handle it and then redirect to refresh the page
    if request.method == "POST" and "comment" in request.POST:
        comment_text = request.POST.get("comment")
        if request.user.is_authenticated and comment_text:
            Comment.objects.create(
                post=post, author=request.user, comment=comment_text, is_active=True
            )
            messages.success(request, "Your comment has been posted!")
        else:
            messages.error(request, "You must be logged in to post a comment.")
        # Redirect so that the new comment is included in the fresh fetch
        return redirect("blog:view_post", slug=post.slug)

    # Fetch related posts based on the category
    category_posts = Post.objects.filter(
        is_active=True, is_published=True, category=post.category
    ).exclude(slug=slug)[:3]

    # Now fetch comments and replies (this will include the newly posted comment after redirect)
    comments_with_replies = handle_comments(post)

    # Prepare the context
    ctx = {
        "post": post,
        "category_posts": category_posts,
        "comments_with_replies": comments_with_replies,
    }

    return render(request, "blog/view_post.html", ctx)


@login_required
def post_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST" and "reply" in request.POST:
        reply_text = request.POST.get("reply")
        if reply_text:
            CommentReply.objects.create(
                comment=comment, author=request.user, reply=reply_text, is_active=True
            )
            messages.success(request, "Your reply has been posted!")
        else:
            messages.error(request, "You cannot post an empty reply.")
    return redirect("blog:view_post", slug=comment.post.slug)


def trending_posts(request):
    return render(
        request,
        "blog/trending_posts.html",
        {
            "all_trending_posts": Post.objects.filter(
                is_active=True, is_published=True
            ).order_by("-views")
        },
    )


def latest_posts(request):
    return render(
        request,
        "blog/latest_posts.html",
        {
            "all_latest_posts": Post.objects.filter(
                is_active=True, is_published=True
            ).order_by("-published_on")
        },
    )


def all_categories(request):
    categories = Category.objects.filter(is_active=True).annotate(
        post_count=Count("posts")
    )
    return render(request, "blog/all_categories.html", {"categories": categories})


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    category_posts = Post.objects.filter(
        is_active=True, is_published=True, category=category
    ).order_by("-published_on")
    return render(
        request,
        "blog/category_posts.html",
        {"category": category, "category_posts": category_posts},
    )
