import os
import random
import time
from io import BytesIO

import django
import requests
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.files.temp import NamedTemporaryFile
from PIL import Image

from app.models import Invitation, ProfileImage, User
from app.utils import get_random_email, get_random_password


def get_random_image_as_bytes():
    url = "https://source.unsplash.com/random/400x300"
    response = requests.get(url)
    return response.content


def get_random_images():
    n = random.randint(1, 6)
    return [get_random_image_as_bytes() for i in range(n)]


def get_random_description():
    return requests.get(
        "https://baconipsum.com/api/?type=meat-and-filler&paras=1&format=text"
    ).text


def run():
    random.seed(time.time())

    for _ in range(5):
        email = get_random_email()
        password = get_random_password()
        print(email)
        user = User.objects.create(email=email, password=password)
        user.description = get_random_description()
        images = get_random_images()
        for image in images:
            profile_image = ProfileImage()
            path = str(random.randint(1, 10000)) + ".png"

            profile_image.user = user
            profile_image.image.save(path, ContentFile(image), save=True)

        user.save()

    users_count = User.objects.count()
    for _ in range(5):
        random_id = random.randint(0, users_count - 1)
        user = User.objects.all()[random_id]
        Invitation.create(user)
