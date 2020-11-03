from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views import View
from django.urls import reverse
from django.shortcuts import render

from .models import Post, Blog, PostIsRead, Subscription
from .forms import PostCreationForm


class BlogList(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        subscriptions = Blog.get_subscriptions_for_user(request.user)
        return render(request, "blogs.html", subscriptions)


class PostList(View):
    def get(self, request, username=None):
        if username is None or not request.user.is_authenticated:
            posts = Post.objects.all().order_by("-pub_date")
        else:
            user = get_object_or_404(User, username=username)
            posts = Post.objects.all().filter(blog__owner=user).order_by("-pub_date")
        return render(request, "posts.html", {"posts": posts})


class PostCreation(View):
    def post(self, request):
        form = PostCreationForm(request.POST)
        if form.is_valid():
            Post.create_from_form(form, request)
            return redirect(reverse("posts"))

    def get(self, request):
        return render(request, "post_edit.html", {"form": PostCreationForm()})


class PostDetail(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if PostIsRead.objects.filter(reader=request.user, post=post).first():
            return render(request, "post_detail.html", {"post": post, "read": True})
        return render(request, "post_detail.html", {"post": post, "read": False})

    def post(self, request, post_id):
        if request.user.is_authenticated:
            post = get_object_or_404(Post, pk=post_id)
            PostIsRead.objects.create(reader=request.user, post=post)
            return redirect(reverse("posts"))
        return redirect(reverse("login"))


class BlogSubscription(View):
    def get(self, request, blog_id):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        blog = get_object_or_404(Blog, id=blog_id)
        is_subscription_action = (
            True if request.META.get("PATH_INFO", None)[1] == "s" else False
        )
        if is_subscription_action:
            Subscription.objects.get_or_create(user=request.user, blog=blog)
            return render(request, "subscription.html", {"action": "subscribed"})
        else:
            PostIsRead.objects.filter(reader=request.user, post__blog=blog).delete()
            Subscription.objects.filter(user=request.user, blog=blog).first().delete()
            return render(request, "subscription.html", {"action": "unsubscribed"})
