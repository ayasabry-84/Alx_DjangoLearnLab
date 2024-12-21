from rest_framework import serializers
from .models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user =  User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user