import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from itertools import chain
from operator import attrgetter
from django.core.paginator import Paginator

from .models import User, Follow, FollowChange, Like, LikeChange,  Post, PostEdition, Comment, CommentChange


def index(request, current="", user_id=0, page=0):
    message = ""
    posts = ""
    try:
        current_user = User.objects.get(pk=user_id)
    except:
        current_user = ""
    following = False
    postTitle = current[0].upper() + current[1:]

    # Following users posts
    if current == "following" and request.user.is_authenticated:
        # Current following users posts
        docs = [set.userTarget.userPosts.all() for set in User.objects.get(pk=request.user.id).follower.all()]
        posts = sorted(
            chain(*docs),
            key=attrgetter('timestamp'),
            reverse=True
        )

    # Current user profile
    elif current == "profile":
        try:
            posts = Post.objects.filter(user = User.objects.get(pk=user_id)).reverse()

            # Count of following and followed users
            following = False
            for u in current_user.followed.all():
                if u.userPointer == request.user:
                    following = True
                    break
        except:
            posts = ""
            message = "The user not found!"

    # All posts
    elif current == "allposts":
        postTitle = "All Posts"
        posts = Post.objects.all().reverse()

    else:
        if current == "following":
            return HttpResponseRedirect(reverse('login'))
        else:
            message = "Request is not exist!"

    # Paginator
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(1 if page == 0 else page)

    return render(request, "network/index.html", {
        "postTitle": postTitle,
        "posts": posts,
        "current_user": current_user,
        "following": following,
        "message": message,
    })

def profile(request, user_id):
    return HttpResponseRedirect(reverse('profile2', args=("profile", user_id)))

@login_required(login_url="login")
def follow(request, user_id):
    if not User.objects.get(pk=user_id) == request.user:
        if not Follow.objects.filter(userPointer = request.user, userTarget = User.objects.get(pk=user_id)).count():
            Follow(userPointer = request.user, userTarget = User.objects.get(pk=user_id)).save()
        else:
            Follow.objects.get(userPointer = request.user, userTarget = User.objects.get(pk=user_id)).delete()
    return HttpResponseRedirect(reverse('profile2', args=("profile", user_id)))

@login_required(login_url="login")
def msgPost(request):
    if request.method != "POST":
        return JsonResponse ({"error": "POST request requited."}, status=400)
    
    data = json.loads(request.body)
    if len(data.get("post").strip()) < 15:
        return JsonResponse ({"error": "Post non-wrapping whitespaces characters are should be more than 14."}, status=400)

    post = Post(
        content = data.get("post"),
        user = request.user
    )
    post.save()
    postEdition = PostEdition(
        post = post,
        content = post.content,
        timestamp = post.timestamp
        )
    postEdition.save()

    return JsonResponse({"message": "Post sent successfully."}, status=201)

@login_required(login_url="login")
def edit(request):
    if request.method != "POST":
        return JsonResponse ({"error": "POST request requited."}, status=400)
    # Initialization
    postId = request.GET.get('id')
    data = json.loads(request.body)
    oldPost = Post.objects.get(pk=postId)
    newText = data.get("post")
    # Validation
    if request.user != oldPost.user:
        return JsonResponse ({"error": "Not own posts edition, Not permitted!"}, status=400)
    if len(data.get("post").strip()) < 15:
        return JsonResponse ({"error": "Post non-wrapping whitespaces characters are should be more than 14."}, status=400)
    
    oldPost.content = newText
    oldPost.save()
    
    edition = PostEdition(
        post = oldPost,
        content = newText,
        timestamp = oldPost.timestamp
    )
    edition.save()
    return JsonResponse({"message": "Post sent successfully."}, status=201)
    
@login_required(login_url="login")
def likeUnlike(request):
    # Initialize
    post_id = request.GET.get('post_id')
    post = Post.objects.get(pk = post_id)
    if post.user.id != request.user.id:
        try:
            currentLike = Like.objects.get(user = request.user, post = post)
            currentLike.likeUnlike = False if currentLike.likeUnlike else True
            currentLike.save()
            like = currentLike
        except:
            newLike = Like(
            user = request.user,
            post = post,
            likeUnlike = True
            )
            newLike.save()
            like = newLike
        # Core
        LikeChange(
            like = like,
            likeUnlike = like.likeUnlike,
            timestamp = like.timestamp
        ).save()

        return JsonResponse({"message": "Like/Unlike updated successfully."}, status=201)
    else:
        return JsonResponse({"message": "User cant like self post."}, status=400)


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
