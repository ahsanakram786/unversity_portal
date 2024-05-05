from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.models import Roles
from django.utils import timezone


# Create your models here.


class User(AbstractUser):
    role = models.ForeignKey(Roles, default=None, null=True, on_delete=models.SET_NULL)
    date_of_birth = models.BigIntegerField(default=None, null=True, verbose_name='Date Of Birth')
    address = models.TextField(default='', null=True, verbose_name='Address')
    city = models.CharField(max_length=100, default='', null=True, verbose_name='City')
    country = models.CharField(max_length=100, default='', null=True, verbose_name='Country')
    image = models.ImageField(upload_to='profile_image/', default='', null=True, verbose_name='Profile Picture URL')

    def __str__(self):
        return f"{self.get_full_name()} [Username: {self.username}] | [Role: {self.role}]"

    class Meta:
        db_table = "User"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user')
    token = models.CharField(max_length=6, db_column='token')  # Assuming token is 6 digits
    expiry_date = models.DateTimeField(db_column='expiry_date')

    def is_expired(self):
        return timezone.now() > self.expiry_date

    class Meta:
        db_table = 'PasswordResetToken'
        ordering = ('-expiry_date',)