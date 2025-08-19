from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User

class UserPublicSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers_count', 'following_count']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        data = UserPublicSerializer(instance).data
        token, _ = Token.objects.get_or_create(user=instance)
        data['token'] = token.key
        return data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        user = authenticate(username=attrs.get('username'), password=attrs.get('password'))
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
        user = self.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return {
            'token': token.key,
            'user': UserPublicSerializer(user).data
        }

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['bio', 'profile_picture']
