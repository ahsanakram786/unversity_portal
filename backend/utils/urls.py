from django.urls import path, include
from .views import *

urlpatterns = [
    path('contact_us', contact_us, name='contact_us'),

]
