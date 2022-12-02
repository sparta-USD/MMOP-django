from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password','phone_number']
        
    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        token['email'] = user.email
        token['username'] = user.username
        return token

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=("username", "password", "phone_number", "email")

    