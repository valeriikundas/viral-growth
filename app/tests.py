import pytest
from django.test import Client
from django.urls import reverse

from .models import Invitation, User


@pytest.fixture
def user1():
    user = User.objects.create(email="email@mail.com", password="password")
    return user


@pytest.fixture
def user2():
    user = User.objects.create(email="verynice@mail.com", password="jamaica999")
    return user


@pytest.fixture
def user3():
    user = User.objects.create(email="tom@mail.com", password="jama123")
    return user


@pytest.fixture
def invitation1(user1: User):
    invitation = Invitation.create(user1)
    return invitation


@pytest.fixture
def invitation2(user2: User):
    invitation = Invitation.create(user2)
    return invitation


@pytest.mark.django_db
class TestUser:
    def test_user_creation(self):
        email = "user1@mail.com"
        user = User.objects.create(email=email)

        assert user.email == email
        assert User.objects.count() == 1
        assert str(user) == f"<User {email}>"

    def test_get_user_by_email(self, user1: User):
        user = User.get_user_by_email(user1.email)

        assert user.email == user1.email

    def test_get_count_of_created_invitations_by_current_user(self, user1: User):
        count = 5
        for _ in range(count):
            Invitation.create(user1)

        assert User.get_count_of_created_invitations(user1) == 5

    def test_get_count_of_used_invitations(self, user1: User, user2: User, user3: User):
        count = 5
        for _ in range(count):
            Invitation.create(user1)

        token = Invitation.objects.all()[0].token
        Invitation.use(token, user2)

        token = Invitation.objects.all()[2].token
        Invitation.use(token, user3)

        assert User.get_count_of_used_invitations(user1)

    def test_user_exists(self, user1):
        assert User.user_exists(user1.email) is True

    def test_get_inviting_user_when_token_is_not_existent(self):
        assert User.get_inviting_user("token") is None

    def test_get_inviting_user_when_it_exists(
        self, user1: User, invitation1: Invitation
    ):
        token = invitation1.token
        user = User.get_inviting_user(token)
        assert isinstance(user, User)


@pytest.mark.django_db
class TestInvitation:
    def test_invitation_creation(self):
        user = User.objects.create(email="user1@mail.com")
        invitation = Invitation.create(user)

        assert invitation.token is not None
        assert Invitation.objects.count() == 1

    def test_invitation_is_marked_as_used(self, invitation1: Invitation, user1: User):
        Invitation.use(invitation1.token, user1)
        invitation1.refresh_from_db()

        assert invitation1.used is True

    def test_get_by_token(self, invitation1: Invitation, invitation2: Invitation):
        invitation = Invitation.get_by_token(invitation1.token)
        assert invitation is not None


@pytest.mark.django_db
def test_invitation_view(user1: User):
    client1 = Client()
    response = client1.post(
        reverse("login"),
        data={"email": user1.email, "password": user1.password},
        follow=True,
    )
    response = client1.get(reverse("invite"))
    invitation_link = response.context.get("invitation_link")

    assert Invitation.objects.first().used == False

    client2 = Client()
    email = "good@good.morning"
    response = client2.post(
        invitation_link, data={"email": email, "password": "password"}, follow=True,
    )
    invitation = Invitation.objects.first()
    assert invitation.used == True
    assert invitation.created_by == user1
    assert invitation.used_by.email == email
