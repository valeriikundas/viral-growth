from django.contrib import admin

from .models import Invitation, ProfileImage, User


class ProfileImageInline(admin.TabularInline):
    model = ProfileImage


class UserInline(admin.ModelAdmin):
    inlines = [ProfileImageInline]


admin.site.register(User, UserInline)
admin.site.register(ProfileImage)
admin.site.register(Invitation)
