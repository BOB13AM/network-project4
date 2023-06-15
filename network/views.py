import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator



from .models import *


def index(request):
    posts = post.objects.order_by("-timestamp").all()
    ptr = Paginator(posts,10)

    page_number = request.GET.get('page')
    page_obj = ptr.get_page(page_number)
    return render(request, "network/index.html",{
        "page_obj":page_obj
    })

@csrf_exempt
@login_required
def newpost(request):
    if request.method == "POST":
        current_user = User.objects.get(pk=request.user.id)

       #to be able to access the variables inside the body that we sent from the JS 
        data = json.loads(request.body)

        # Get contents of post
        new_post = data.get("post", "")

        #check if i am receiving the values from the user and add the new task to the model
        if new_post and current_user:
            add_post = post(user=current_user, body=new_post)
            add_post.save()
            return JsonResponse({"message": "Post Added successfully."}, status=201)
        else:
            return JsonResponse({"error": "Missing Info"}, status=400)
        
@csrf_exempt       
def user_page(request,userid):
        if request.method=="POST":
            targetuser = User.objects.get(pk=userid)
            all_user_posts = targetuser.user_post.order_by("-timestamp").all()
            ptr = Paginator(all_user_posts,10)

            page_number = request.GET.get('page')
            page_obj = ptr.get_page(page_number)

            return render(request, "network/userpage.html",{
                        "page_obj":page_obj,
                        "user": targetuser,
                        
                    })
        else:
            targetuser = User.objects.get(pk=userid)
            all_user_posts = targetuser.user_post.order_by("-timestamp").all()
            ptr = Paginator(all_user_posts,10)

            page_number = request.GET.get('page')
            page_obj = ptr.get_page(page_number)

            return render(request, "network/userpage.html",{
                        "page_obj":page_obj,
                        "user": targetuser,
                        
                    })

@csrf_exempt  
def follow_feature(request,id):
    if request.method == "PUT":

        #current user 
        current_user = User.objects.get(pk=request.user.id)
        # target user to(follow/unfollow)
        target_user = User.objects.get(pk=id)

        #to be able to access the variables inside the body that we sent from the JS 
        data = json.loads(request.body)

        # Get contents of post
        follow = data.get("follow", "")
        unfollow = data.get("unfollow", "")

        if follow and id and not unfollow:
            current_user.user_followers.add(target_user)
            return JsonResponse({"message": "Follow User successful."}, status=201)

        elif unfollow and id and not follow:
            current_user.user_followers.remove(target_user)
            return JsonResponse({"message": "Unfollowed User successful."}, status=201)

@csrf_exempt
@login_required
def following(request):
    #current user 
    current_user = User.objects.get(pk=request.user.id)
    user_following = current_user.user_following()
    all_posts = post.objects.order_by("-timestamp").filter(user__in=user_following)
    ptr = Paginator(all_posts,10)

    page_number = request.GET.get('page')
    page_obj = ptr.get_page(page_number)
    return render(request, "network/following.html",{
        "page_obj":page_obj
    })

@csrf_exempt
@login_required
def edit(request):
     if request.method == "PUT":
         #to be able to access the variables inside the body that we sent from the JS 
        data = json.loads(request.body)

        # Get contents of post
        id = data.get("target_id", "")
        newcontent = data.get("content","")

        update = post.objects.get(pk=id)

        update.body = newcontent

        update.save()
        
        return JsonResponse({"message": "Update Post Successful."}, status=201)


@csrf_exempt
@login_required
def like_feature(request):
     if request.method == "PUT":
        current_user = User.objects.get(pk=request.user.id)

        #to be able to access the variables inside the body that we sent from the JS 
        data = json.loads(request.body)

        # Get contents of post
        id = data.get("target_id", "")
        like = data.get("like", "")
        unlike = data.get("unlike", "")

        if like and id and not unlike:
            target_post = post.objects.get(pk=id)
            target_post.user_likes.add(current_user)
            return JsonResponse(target_post.serialize())
        elif unlike and id and not like:
            target_post = post.objects.get(pk=id)
            target_post.user_likes.remove(current_user)
            return JsonResponse(target_post.serialize())    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
