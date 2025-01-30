from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("all_blogs/", views.all_blogs, name="all_blogs"),
    path("latest_posts/", views.latest_posts, name="latest_posts"),
    path("trending_posts/", views.trending_posts, name="trending_posts"),
    path("all_categories/", views.all_categories, name="all_categories"),
    path("<slug:slug>/", views.view_post, name="view_post"),
    path("category/<slug:category_slug>/", views.category_posts, name="category_posts"),
    path("<slug:slug>/post_comment/", views.view_post, name="post_comment"),
    path("post_reply/<int:comment_id>/", views.post_reply, name="post_reply"),
]
