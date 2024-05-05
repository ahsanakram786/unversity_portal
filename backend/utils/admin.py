from django.contrib import admin
from .models import Roles, ContactUs
from django.contrib.auth.models import Group
# from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

# Register your models here.
admin.site.register(Roles)

# Register your models here.
admin.site.register(ContactUs)

# Unregister Group models from admin
admin.site.unregister(Group)
