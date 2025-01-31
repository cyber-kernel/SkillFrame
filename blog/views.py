from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import F
from .models import Post, Comment, CommentReply, Category
from django.contrib.auth.decorators import login_required


def all_blogs(request):
    all_posts = Post.objects.filter(is_active=True, is_published=True).order_by(
        "published_on"
    )
    return render(request, "blog/all_blogs.html", {"all_posts": all_posts})


def handle_comments(request, post):
    """Handles comment retrieval and submission for a blog post."""
    # Fetch active comments and their replies
    comments = post.comments.filter(is_active=True)
    comment_replies = CommentReply.objects.filter(is_active=True)

    # Creating a dictionary of comments and their replies
    comments_with_replies = [
        {"comment": comment, "replies": comment_replies.filter(comment=comment)}
        for comment in comments
    ]

    # Handle comment submission
    if request.method == "POST" and "comment" in request.POST:
        comment_text = request.POST.get("comment")
        if request.user.is_authenticated and comment_text:
            Comment.objects.create(
                post=post, author=request.user, comment=comment_text, is_active=True
            )
            messages.success(request, "Your comment has been posted!")
        else:
            messages.error(request, "You must be logged in to post a comment.")

    return comments_with_replies


def view_post(request, slug):
    """Handles blog post view and interactions."""
    # Fetch the post based on the slug
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

    # Fetch related posts based on the category
    category_posts = Post.objects.filter(
        is_active=True, is_published=True, category=post.category
    ).exclude(slug=slug)[:3]

    # Fetch comments using the new function
    comments_with_replies = handle_comments(request, post)

    # Prepare the context
    ctx = {
        "post": post,
        "category_posts": category_posts,
        "comments_with_replies": comments_with_replies,
    }

    return render(request, "blog/view_post.html", ctx)


@login_required
def post_reply(request, comment_id):
    # Fetch the comment based on the comment_id
    comment = Comment.objects.get(id=comment_id)

    if request.method == "POST" and "reply" in request.POST:
        reply_text = request.POST.get("reply")

        if reply_text:
            # Create a new reply for the comment
            CommentReply.objects.create(
                comment=comment, author=request.user, reply=reply_text, is_active=True
            )
            messages.success(request, "Your reply has been posted!")
        else:
            messages.error(request, "You cannot post an empty reply.")

    # After posting the reply, redirect back to the post page
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
        post_count=Count("posts")  # noqa: F821
    )
    return render(request, "blog/all_categories.html", {"categories": categories})


def category_posts(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    category_posts = Post.objects.filter(
        is_active=True, is_published=True, category=category
    ).order_by("-published_on")
    return render(
        request,
        "blog/category_posts.html",
        {"category": category, "category_posts": category_posts},
    )
