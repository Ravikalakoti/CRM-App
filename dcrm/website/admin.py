from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Record, BlogPost, UserProfile, Message, Education


class UserProfileInline(admin.StackedInline):
    model = UserProfile

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]


admin.site.register(Record)
admin.site.register(BlogPost)
admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(Education)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)