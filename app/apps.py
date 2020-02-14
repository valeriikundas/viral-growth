from django.apps import AppConfig

# bad collision of names there. I did not notice it in the beginning and decided to not rename
# left it as it is a very small project and did not cause any errors
class AppConfig(AppConfig):
    name = "app"
