from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.shortcuts import redirect, render, reverse

from .forms import ProfileEditForm
from .models import Invitation, ProfileImage, User

# shows profile description and images of all users
# I left it without pagination, but in real projects,
# pagination is of course required
def index_view(request: HttpRequest):
    context = {"users": User.get_users_data()}
    return render(request, "app/index.html", context)


# view that created invitation link for a new user
@login_required
def invite_view(request):
    invitation = Invitation.create(request.user)
    invitation_link = reverse("login", kwargs={"token": invitation.token})

    context = {"invitation_link": invitation_link}
    return render(request, "app/invite.html", context)


# login and signup are unified.
# when a new user tries to login, his account is created.
def login_view(request, token=None):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email is None or password is None:
            return redirect("index", error="specify email and password")

        if User.user_exists(email):
            user = authenticate(request, email=email, password=password)
            if user is None:
                return render(
                    request,
                    "app/index.html",
                    context={"error": "wrong email or password"},
                )

            login(request, user)
            return redirect("index")

        user = User.objects.create(email=email, password=password)

        if token is not None:
            Invitation.use(token, user)

        login(request, user)
        return redirect("index")

    if request.method == "GET":
        if token is not None:
            invitation = Invitation.get_by_token(token)
            if invitation is None:
                return render(
                    request, "app/index.html", context={"error": "wrong token"}
                )

        return render(request, "app/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


@login_required
def profile_view(request, profile_id=None):
    if profile_id is None:
        profile_id = request.user.id
    user: User = User.objects.get(id=profile_id)

    context = {
        "description": user.description,
        "profile_images": user.get_image_urls(),
        "count_created_invitations": user.get_count_of_created_invitations(),
        "count_used_invitations": user.get_count_of_used_invitations(),
    }
    return render(request, "app/profile.html", context)


@login_required
def profile_edit_view(request):
    user: User = request.user

    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES)
        if form.is_valid():
            description = form.cleaned_data.get("description")
            if description is not None:
                user.description = description

            new_image = form.cleaned_data.get("new_image")
            if new_image is not None:
                ProfileImage.create(user, new_image)

            user.save()
            return redirect("profile")
    else:
        form = ProfileEditForm()

    context = {"form": form}
    return render(request, "app/profile_edit.html", context)
