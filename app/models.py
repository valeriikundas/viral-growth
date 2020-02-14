from django.conf import settings
from typing import List
from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from .utils import get_random_string, token_generator


class User(AbstractUser):
    email = models.EmailField(null=False)
    description = models.TextField(blank=True, null=False)

    def __str__(self):
        return f"<User {self.email}>"

    def save(self, *args, **kwargs):
        self.username = self.email
        super(User, self).save(*args, **kwargs)

    @staticmethod
    def get_user_by_email(email: str):
        return User.objects.filter(email=email).first()

    def get_count_of_created_invitations(self):
        return Invitation.objects.filter(created_by=self.id).count()

    def get_count_of_used_invitations(self):
        return (
            Invitation.objects.filter(created_by=self.id).exclude(used_by=None).count()
        )

    @staticmethod
    def user_exists(email: str):
        user = User.objects.filter(email=email).first()
        return user is not None

    @staticmethod
    def get_inviting_user(token: str):
        invitation = Invitation.objects.filter(token=token).first()
        if invitation is None:
            return None
        return invitation.created_by

    def get_image_urls(self):
        return [img.image.url for img in self.images.all()]

    @staticmethod
    def get_users_data() -> List["User"]:
        return [
            {
                "email": user.email,
                "description": user.description,
                "images": user.get_image_urls(),
            }
            for user in User.objects.all()
        ]


class ProfileImage(models.Model):
    image = models.ImageField(upload_to="images/")
    user = models.ForeignKey(User, related_name="images", on_delete=models.CASCADE)

    def __str__(self):
        return f"<ProfileImage {self.image}>"

    @staticmethod
    def create(user: User, new_image: InMemoryUploadedFile):
        profile_image = ProfileImage(user=user)
        name = ProfileImage.random_filename()
        profile_image.image.save(name, new_image)
        profile_image.save()

    @staticmethod
    def random_filename():
        return f"{get_random_string()}.png"


class Invitation(models.Model):
    token = models.TextField(max_length=100, null=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_invitations",
        on_delete=models.CASCADE,
    )
    used_by = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="joined_invitation",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return f"<Invitation {self.token} {str(self.used)}"

    @property
    def used(self) -> bool:
        return self.used_by is not None

    @staticmethod
    def create(user: User) -> "Invitation":
        token = token_generator.get()
        invitation = Invitation(token=token, created_by=user)
        invitation.save()
        return invitation

    @staticmethod
    def use(token: str, user: User):
        invitation = Invitation.objects.get(token=token)
        invitation.used_by = user
        invitation.save()

    @staticmethod
    def get_by_token(token: str) -> "Invitation":
        return Invitation.objects.filter(token=token).first()


