from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.models import Roles
# Create your models here.


class User(AbstractUser):
    role = models.ForeignKey(Roles, default=None, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.get_full_name()} [Username: {self.username}] | [Role: {self.role}]"

    class Meta:
        db_table = "User"
