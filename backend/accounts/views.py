from django.shortcuts import render
from rest_framework.response import Response
from utils.handlers.request_handlers import DRHandler
from rest_framework.status import *

DR_handler = DRHandler()
# Create your views here.


@DR_handler.public_rest_call(allowed_methods=['POST'])
def login(request):

    return Response(data={
        'user': request.user.username
    }, status=HTTP_200_OK)


@DR_handler.authenticate_rest_call(allowed_methods=['POST'])
def update_user(request):

    return Response(data={
        'user': request.user.username
    }, status=HTTP_200_OK)