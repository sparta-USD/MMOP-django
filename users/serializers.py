from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User
import re


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style = {'input_type': 'password'},
        write_only = True
    )
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'phone_number']
        
    def create(self, validated_data):
        del(validated_data['password2'])
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user
    
    def validate_phone_number(self, value):
        is_phone_number_valid = re.match("\d{3}-\d{3,4}-\d{4}", value)
        if not is_phone_number_valid:
            raise serializers.ValidationError(
                detail={
                    "message" : "전화번호를 확인해 주세요."
                })
        return value
    
    def validate_password(self, value):
        is_password_valid = re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,21}$", value)
        
        if not (8 <= len(value) <= 20):
            raise serializers.ValidationError(
                detail={
                    "message" : "비밀번호는 8~20자 이어야 합니다."
                })
            
        if not is_password_valid:
            raise serializers.ValidationError(
                detail={
                    "message" : "비밀번호는 영어 대문자, 소문자, 숫자, 특수문자(@$!%*#?&) 하나씩 꼭 포함하여야 합니다."
                })
        return value
    
    def validate(self, attrs):
        if not attrs["password"]:
            raise serializers.ValidationError(
                detail={
                    "message" : "비밀번호를 입력해 주세요."
                })
        
        if not attrs["password"] == attrs["password2"]:
            raise serializers.ValidationError(
                detail={
                    "message" : "비밀번호가 일치하지 않습니다."
                })
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        token['email'] = user.email
        token['username'] = user.username
        return token

class MypageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=("username", "password", "phone_number", "email")

    