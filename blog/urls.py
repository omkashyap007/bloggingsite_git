from django.urls import path 
from . import views
from django.contrib.auth.models import User
from blog import views as blog_views
from blog.views import (
                        PostListView ,
                        PostDetailView ,
                        PostDeleteView ,
                        UserPostListView
                        )

urlpatterns = [
    path("" , PostListView.as_view() , name = "blog-home"),
    path("post/<int:pk>/" , PostDetailView.as_view() , name = "post-detail"),
    path("post/new/" , blog_views.CreatePost , name = "post-create"),
    path("post/<str:username>" , blog_views.UserPostListView , name = "user-posts"),
    path("post/<int:pk>/like/" , blog_views.PostLike , name = "post-like"),
    path("post/<int:pk>/comment" , blog_views.PostComment , name = "post-comment") , 
    path("post/<int:pk>/update/" , blog_views.PostUpdate , name = "post-update" ),
    path("post/<int:pk>/delete/" , PostDeleteView.as_view() , name = "post-delete"),
    path("about/" , views.about , name = "blog-about"),
    path("post/delete-comment/<int:pk>/<int:post_pk>/" , blog_views.DeleteComment , name = "post-delete-comment"),
    path("blog/search/" , blog_views.SearchData , name = "form-search" ) ,
    path("blog/hashtag/<str:hashtag>" , blog_views.BlogTypeView , name = "post-hashtag") , 
    path("follow/<int:userid>/" , blog_views.FollowUser , name = "follow-user") ,
    path("unfollow/<int:userid>/" , blog_views.UnFollowUser , name = "unfollow-user") ,
    path("search-input/" , blog_views.SearchData , name = "search-input" ) ,
]