import base64

from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from  utils.models import Roles
User_Model = get_user_model()


class JWTObtainTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token


class JWTTokenView(TokenObtainPairView):
    serializer_class = JWTObtainTokenPairSerializer


class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(allow_blank=True, )
    image = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        # Decode the base64 image data
        role_ = Roles.objects.filter(name='STUDENT')
        validated_data['role'] = role_.first()

        image_data = validated_data.get('image', None)
        if image_data:
            type_format, img_str = image_data.split(';base64,')
            ext = type_format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(img_str), name=f"{validated_data['username']}.{ext}")

            validated_data['image'] = image_data

        return User_Model.objects.create_user(**validated_data, is_active=True)

    def update(self, instance, validated_data):
        # instance = super(UserSerializers, self).update(instance, validated_data)
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.date_of_birth = validated_data.get('date_of_birth')
        instance.address = validated_data.get('address')
        instance.city = validated_data.get('city')
        instance.country = validated_data.get('country')
        if 'password' in validated_data and validated_data['password'] != '':
            instance.set_password(validated_data['password'])
        else:
            validated_data.pop('password')

        if 'email' in validated_data and validated_data['email'] == '':
            validated_data.pop('email')
        else:
            instance.email = validated_data.get('email')

        if 'image' in validated_data and (not validated_data['image'] or validated_data['image'] == ''):
            validated_data.pop('image')
        else:
            # Decode the base64 image data
            image_data = validated_data.get('image', None)
            if image_data:
                type_format, img_str = image_data.split(';base64,')
                ext = type_format.split('/')[-1]
                image_data = ContentFile(base64.b64decode(img_str), name=f"{validated_data['username']}.{ext}")

                validated_data['image'] = image_data
            instance.image = validated_data.get('image')

        instance.save()
        return instance

    def to_representation(self, instance):
        data = super(UserSerializers, self).to_representation(instance)

        if 'password' in data:
            data.pop('password')
        data.pop('date_joined')

        if 'image' in data and data['image'] is not None and data['image'] != "":
            data['image'] = f"{settings.MEDIA_URL}{data['image']}"

        return data

    class Meta:
        model = User_Model
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'user_permissions': {'write_only': True},
            'groups': {'write_only': True}
        }
