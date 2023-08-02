from django.contrib import admin
from .models import Record, BlogPost, UserProfile, Message

admin.site.register(Record)
admin.site.register(BlogPost)
admin.site.register(UserProfile)
admin.site.register(Message)