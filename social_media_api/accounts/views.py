from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics

from .serializers import (
    RegisterSerializer, LoginSerializer, UserPublicSerializer, ProfileUpdateSerializer
)
from .models import User

from .serializers import UserMiniSerializer

User = get_user_model()

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
    
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id: int):
        if request.user.id == user_id:
            return Response({"detail": "You cannot follow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            target = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."},
                            status=status.HTTP_404_NOT_FOUND)

        if request.user.following.filter(pk=target.pk).exists():
            # Idempotent
            data = UserMiniSerializer(target, context={"request": request}).data
            return Response({"detail": "Already following.", "user": data},
                            status=status.HTTP_200_OK)

        request.user.following.add(target)
        data = UserMiniSerializer(target, context={"request": request}).data
        return Response({"detail": "Followed successfully.", "user": data},
                        status=status.HTTP_201_CREATED)


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id: int):
        if request.user.id == user_id:
            return Response({"detail": "You cannot unfollow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            target = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."},
                            status=status.HTTP_404_NOT_FOUND)

        if request.user.following.filter(pk=target.pk).exists():
            request.user.following.remove(target)
            return Response(status=status.HTTP_204_NO_CONTENT)

        # Idempotent
        return Response({"detail": "You were not following this user."},
                        status=status.HTTP_200_OK)
