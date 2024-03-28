from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

User_Model = get_user_model()

class UserSerializers(ModelSerializer):

    class Meta:
        model = User_Model
        fields = '__all__'


