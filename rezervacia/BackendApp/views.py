from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .serializers import RegisterSerializer, LoginSerializer
import hashlib
from .models import User

@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        # Hash the password
        hashed_password = hashlib.sha256(serializer.validated_data['password_hash'].encode()).hexdigest()
        serializer.validated_data['password_hash'] = hashed_password

        # Save the user
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            user = User.objects.get(username=username, password_hash=hashed_password)
            return Response({"message": "Login successful", "user": {"username": user.username, "email": user.email, "phone": user.phone}}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)