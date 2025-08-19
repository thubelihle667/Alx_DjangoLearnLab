from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics

from .serializers import (
    RegisterSerializer, LoginSerializer, UserPublicSerializer, ProfileUpdateSerializer
)
from .models import User

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.to_representation(user), status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return Response(UserPublicSerializer(request.user).data)

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
