from django.db import models

# Create your models here.


class Roles(models.Model):
    name = models.CharField(default=None, max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "Roles"