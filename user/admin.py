from django.contrib import admin
# Register your models here.
from user.models import User
from rest_framework.authtoken.models import Token

admin.site.register(User)
admin.site.register(Token)
