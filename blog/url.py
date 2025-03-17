from django.contrib import admin
from django.urls import path,include
from .views import create_user,Login,commentListView
from . import views


urlpatterns = [
   path("create/",create_user,name="create_user"),
   path("login/",Login,name="login"),
   path('verify-token/', views.verify_token, name='verify_token'),
   path('forgot-password/',views.forgot,name="forgot"),
   path('reset_passward/',views.reset_password,name="reset_passward"),
   path('addpost/',views.addpost,name="addpost"),
   path("post/",views.post,name="post"),
   path('blog_list/',views.blog_list,name="blog_list"),
   path("profile_pic/",views.profile_pic,name="profile_pic"),
   path("profile/",views.profile,name="profile"),
   path("user_post/",views.user_post,name="user_post"),
   path("search_post/",views.search,name="search_post"),
   path("posts/<int:post_id>/comments",commentListView.as_view(),name='comment'),
   path("delete/comments/<int:cmt_id>/",views.delete,name="delete")
]