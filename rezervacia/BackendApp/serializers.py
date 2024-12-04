from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password_hash', 'phone']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()