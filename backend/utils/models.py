from django.db import models

# Create your models here.


class Roles(models.Model):
    name = models.CharField(default=None, max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "Roles"


class ContactUs(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, db_column='name', verbose_name='Name')
    email = models.EmailField(null=False, blank=False, db_column='email', verbose_name='Email')
    subject = models.CharField(max_length=255, null=False, blank=False, db_column='subject', verbose_name='Enquiry Subject')
    message = models.TextField(null=False, blank=False, db_column='message', verbose_name='Enquiry Message')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    def __str__(self):
        return f"{self.name} - {self.subject} - {str(self.created_at.date())}"

    class Meta:
        db_table = "ContactUs"
        ordering = ("-created_at",)
