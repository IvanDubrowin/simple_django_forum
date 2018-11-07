from django.contrib import admin
from .models import ForumUser, Thread, Post

admin_site = admin.AdminSite(name='admin')
admin_site.register([ForumUser, Thread, Post])
