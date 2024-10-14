"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import LitReview.views
import authentication.views

urlpatterns = [
    path("admin/", admin.site.urls),
    # authentication
    path(
        "",
        LoginView.as_view(
            template_name="authentication/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "change-password/",
        PasswordChangeView.as_view(
            template_name="authentication/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "change-password-done/",
        PasswordChangeDoneView.as_view(
            template_name="authentication/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("signup/", authentication.views.signup_page, name="signup"),
    #  LitReview
    # Followers
    path("follow/", LitReview.views.follow_user, name="follow_user"),
    path("unfollow/", LitReview.views.unfollow_user, name="unfollow_user"),
    path("followers/", LitReview.views.followers, name="followers"),
    # creat a ticket
    path("create-ticket/", LitReview.views.create_ticket, name="create_ticket"),
    path(
        "create-review/<int:ticket_id>/",
        LitReview.views.create_review,
        name="create_review_with_ticket",
    ),
    path(
        "create-review/", LitReview.views.create_review, name="create_review"
    ),  # Conserve cette ligne
    # edit ticket and review
    path(
        "edit-ticket/<int:ticket_id>/edit",
        LitReview.views.edit_ticket,
        name="edit_ticket",
    ),
    path(
        "edit-review/<int:review_id>/edit",
        LitReview.views.edit_review,
        name="edit_review",
    ),
    # delete ticket and review
    path(
        "delete-ticket/<int:ticket_id>/delete",
        LitReview.views.delete_ticket,
        name="delete_ticket",
    ),
    path(
        "delete-review/<int:review_id>/delete",
        LitReview.views.delete_review,
        name="delete_review",
    ),
    path("my-posts/", LitReview.views.my_posts, name="my_posts"),
    path("home/", LitReview.views.home, name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
