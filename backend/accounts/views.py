import json
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.response import Response

from utils.handlers.email_handlers import send_email
from utils.handlers.request_handlers import DRHandler
from rest_framework.status import *

from utils.utils import generate_random_token
from .models import PasswordResetToken
from .serializers import UserSerializers

UserModel = get_user_model()

DR_handler = DRHandler()
# Create your views here.


@DR_handler.public_rest_call(allowed_methods=['POST'])
def login(request):

    return Response(data={
        'user': request.user.username
    }, status=HTTP_200_OK)


@DR_handler.public_rest_call(allowed_methods=['POST'])
def add_user(request):
    serializer_ = ''
    data = json.loads(request.body)

    if data:
        try:
            serializer_ = UserSerializers(data=data, many=False)
            if serializer_.is_valid(raise_exception=True):
                serializer_.save()
                return Response(data={
                    'message': "Student Registered!"
                }, status=HTTP_200_OK)
        except Exception as ex:
            return Response(data={
                'error': serializer_.errors
            }, status=HTTP_400_BAD_REQUEST)


@DR_handler.authenticate_rest_call(allowed_methods=['GET'])
def get_user(request):

    try:
        user_ = UserModel.objects.filter(id=request.user.id)
    except Exception as ex:
        return Response(data={
            'message': 'Invalid User'
        }, status=HTTP_400_BAD_REQUEST)

    serializer_ = UserSerializers(user_, many=True)
    return Response(data={
        'data': serializer_.data
    }, status=HTTP_200_OK)


@DR_handler.authenticate_rest_call(allowed_methods=['POST'])
def update_user(request):
    serializer_ = ''
    data = json.loads(request.body)

    if data:
        user_ = UserModel.objects.filter(username=data.get('username', None)).first()
        serializer_ = UserSerializers(user_, data=data, partial=True)
        if serializer_.is_valid(raise_exception=True):
            serializer_.save()
            return Response(data={
                'message': "User Updated!"
            }, status=HTTP_200_OK)
    return Response(data={
        'error': serializer_.errors
    }, status=HTTP_400_BAD_REQUEST)


@DR_handler.public_rest_call(allowed_methods=['POST'])
def send_reset_password(request):
    email = request.data.get('email', None)
    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        return Response({'message': 'User does not exist'}, status=HTTP_400_BAD_REQUEST)

    # Generate a random 6-digit token
    token = generate_random_token()

    # Save the token with expiry date (e.g., 30 minutes from now)
    expiry_date = timezone.now() + timezone.timedelta(minutes=30)
    PasswordResetToken.objects.create(user=user, token=token, expiry_date=expiry_date)

    # Send reset password email
    if send_email("Token", f"{token}", user.email):

        return Response({'message': "Reset password email sent. \nif doen't find you email in you inbox, "
                                    "please check you spam box."}, status=HTTP_200_OK)
    else:
        return Response({'message': 'Email Token can not sent. Server Error.'}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@DR_handler.public_rest_call(allowed_methods=['POST'])
def validate_reset_token(request):
    token = request.data.get('token', None)
    password = request.data.get('password', None)
    confirm_password = request.data.get('confirm_password', None)

    # Find the token in the database
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        return Response({'message': 'Invalid or expired token'}, status=HTTP_400_BAD_REQUEST)

    if reset_token.is_expired():
        return Response({'message': 'Token has expired'}, status=HTTP_400_BAD_REQUEST)

    # Validate password and confirm password
    if password != confirm_password:
        return Response({'message': 'Passwords do not match'}, status=HTTP_400_BAD_REQUEST)

    # Update user's password and delete the token
    user = reset_token.user
    user.set_password(password)
    user.save()
    reset_token.delete()

    return Response({'message': 'Password reset successfully'}, status=HTTP_200_OK)