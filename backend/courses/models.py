from django.contrib.auth import get_user_model
from django.db import models
from utils.utils import get_code

UserModel = get_user_model()

# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=100, null=True, verbose_name='Category Name')


class Module(models.Model):
    """
    Modules Model that can have multiple courses init.
    """
    AVAILABILITY_CHOICES = [
        ('open', 'Open for registration'),
        ('closed', 'Closed for registration'),
    ]

    name = models.CharField(max_length=255, verbose_name='Name of the module')
    code = models.CharField(max_length=255, unique=True, verbose_name='Code')
    credit = models.IntegerField(verbose_name='Credit')
    category = models.CharField(max_length=100, verbose_name='Category')
    description = models.TextField(verbose_name='Description')
    availability = models.CharField(
        max_length=10,
        choices=AVAILABILITY_CHOICES,
        default='open',
        verbose_name='Availability'
    )
    course_allowed = models.ManyToManyField('Course', related_name='modules', verbose_name='Courses allowed to register')

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):

        self.code = f"{self.name}/{get_code()}"

        super().save(*args, **kwargs)


class Course(models.Model):
    """
    Represents a course that can have multiple modules offered.
    """
    name = models.CharField(max_length=255, verbose_name='Name of the course')
    code = models.CharField(max_length=255, unique=True, verbose_name='Code')
    description = models.TextField(verbose_name='Description')

    def __str__(self):
        return f"{self.code} - {self.name}"


class StudentModuleRegistration(models.Model):
    student = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='registrations')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} registered for {self.module.name} on {self.registration_date}"

    class Meta:
        db_table = 'StudentModuleRegistration'
        unique_together = ('student', 'module')
        ordering = ['-registration_date']