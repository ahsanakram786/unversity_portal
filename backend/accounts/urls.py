from django.urls import path, include
from .views import *
urlpatterns = [
    # path('login', login, name='login'),
    path('add_user', add_user, name='add_user'),
    path('update_user', update_user, name='update_user'),
    path('get_user', get_user, name='get_user'),

    # Password Reset
    path('send_reset_password', send_reset_password, name='send_reset_password'),
    path('validate_reset_token', validate_reset_token, name='validate_reset_token'),

    # contact us
    path('contact_us', validate_reset_token, name='contact_us'),
]
