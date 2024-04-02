from django.urls import path, include
from .views import *
urlpatterns = [
    path('login', login, name='login'),
    path('update_user', update_user, name='update_user'),

]
