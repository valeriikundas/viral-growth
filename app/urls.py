from django.urls import path

from .views import (
    index_view,
    invite_view,
    login_view,
    logout_view,
    profile_edit_view,
    profile_view,
)

urlpatterns = [
    path("", index_view, name="index"),
    path("invite/", invite_view, name="invite"),
    path("profile/", profile_view, name="profile"),
    path("profile/<int:profile_id>/", profile_view, name="profile"),
    path("profile/edit/", profile_edit_view, name="profile_edit"),
    path("login/", login_view, name="login"),
    path("login/<str:token>/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
