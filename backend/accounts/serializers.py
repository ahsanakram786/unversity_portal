from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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


class UserSerializers(ModelSerializer):
    class Meta:
        model = User_Model
        fields = '__all__'
