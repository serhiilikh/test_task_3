from .views import PostList, PostCreation, PostDetail, BlogSubscription, BlogList
from django.contrib.auth import views
from django.urls import path


urlpatterns = [
    path("", PostList.as_view(), name="posts"),
    path("post/<int:post_id>/", PostDetail.as_view(), name="post_detail"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("create_post/", PostCreation.as_view(), name="create_post"),
    path("subscribe/<int:blog_id>/", BlogSubscription.as_view(), name="subscribe"),
    path("unsubscribe/<int:blog_id>/", BlogSubscription.as_view(), name="unsubscribe"),
    path("blogs/", BlogList.as_view(), name="blogs"),
    path("blog/<str:username>/", PostList.as_view(), name="posts"),
]
