from django.contrib import admin
from .models import User


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    exclude = ["image", "groups", "user_permissions"]


admin.site.register(User, UserAdmin)
