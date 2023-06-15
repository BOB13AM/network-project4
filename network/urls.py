
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("follow_feature/<int:id>", views.follow_feature, name="follow_feature"),
    path("<int:userid>", views.user_page,name="user_page"),
    path("following", views.following, name="following"),
    path("edit", views.edit, name="edit"),
    path("like_feature", views.like_feature, name="like_feature")

]
