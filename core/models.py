from django.contrib.auth.models import AbstractUser, User
from django.db import models


class Blog(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner.username}'s blog"

    @staticmethod
    def create_if_doesnt_exist(user):
        try:
            blog = Blog.objects.get(owner=user)
        except Blog.DoesNotExist:
            blog = Blog.objects.create(owner=user)
        return blog

    @staticmethod
    def get_subscriptions_for_user(user):
        subscribed_to = []
        not_subscribed_to = []
        for blog in Blog.objects.all():
            if Subscription.objects.filter(blog=blog, user=user).first():
                subscribed_to.append(blog)
            else:
                not_subscribed_to.append(blog)
        return {"subscribed_to": subscribed_to, "not_subscribed_to": not_subscribed_to}


class Post(models.Model):
    title = models.CharField(max_length=1000, blank=False)
    content = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @staticmethod
    def create_from_form(form, request):
        post = form.save(commit=False)
        post.author = request.user
        post.blog = Blog.create_if_doesnt_exist(request.user)
        post.save()


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)


class PostIsRead(models.Model):
    reader = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
