from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from users.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from perfume.models import Review
from perfume.serializers import ReviewSerializer, PerfumeSerializer
from custom_perfume.serializers import CustomPerfumeSerializer

import re

from django.shortcuts import render, redirect

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from .tokens import account_activation_token
from django.core import mail
from django.conf import settings
from django.utils.html import strip_tags

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, validators=[UniqueValidator(queryset=get_user_model().objects.all(), message="이 이메일은 이미 사용중입니다.")])
    username = serializers.CharField(max_length=15, validators=[UniqueValidator(queryset=get_user_model().objects.all(), message="이 닉네임은 이미 사용중입니다.")])
    password2 = serializers.CharField(
        style = {'input_type': 'password'},
        write_only = True
    )
    class Meta:
        model = User
        fields = ['email', 'email_valid', 'username', 'password', 'password2', 'phone_number']
        
    def create(self, validated_data):
        del(validated_data['password2'])
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.email_valid = False
        user.is_active = False
        user.save()


        # 인증 이메일 전송
        
        message = render_to_string('email_valid.html', {
            'user': user,
            'domain': 'http://127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        plain_message = strip_tags(message)
        mail_subject = "MMOP 이메일 인증 링크 보내드립니다"
        to_email = user.email
        mail.send_mail(mail_subject, plain_message, settings.EMAIL_HOST_USER, [to_email], html_message=message)

        return user
    
    def validate_phone_number(self, value):
        if value:
            is_phone_number_valid = re.match("\d{3}-\d{3,4}-\d{4}", value)
            if not is_phone_number_valid:
                raise serializers.ValidationError("전화번호를 확인해 주세요.")
        return value
    
    def validate_password(self, value):
        is_password_valid = re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,21}$", value)
        
        if not (8 <= len(value) <= 20):
            raise serializers.ValidationError("비밀번호는 8~20자 이어야 합니다.")
            
        if not is_password_valid:
            raise serializers.ValidationError("비밀번호는 영어 대문자, 소문자, 숫자, 특수문자(@$!%*#?&) 하나씩 꼭 포함하여야 합니다.")
        return value
    
    def validate(self, attrs):
        if not attrs["password"]:
            raise serializers.ValidationError({"password":"비밀번호를 입력해 주세요."})
        
        if not attrs["password"] == attrs["password2"]:
            raise serializers.ValidationError({"password2":"비밀번호가 일치하지 않습니다."})
        return attrs
    


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            user = get_user_model().objects.get(email = attrs["email"])
        # 이메일이 존재하지 않을 때
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("이메일에 맞는 계정이 존재하지 않습니다.")
        
        # 패스워드가 일치하지 않을 때
        if not check_password(attrs["password"], user.password):
            raise exceptions.AuthenticationFailed("비밀번호가 일치하지 않습니다.")
        
        # 이메일 검증을 하지 않았을 때
        if not user.email_valid:
            raise exceptions.AuthenticationFailed(f"인증메일이 {user.email}로 전송되었습니다. 이메일을 확인해주세요.")
        
        data = super().validate(attrs)
        return data
        
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        token['email'] = user.email
        token['username'] = user.username
        return token

class MypageSerializer(serializers.ModelSerializer):
    user_reviews = serializers.SerializerMethodField()
    like_perfume = PerfumeSerializer(many=True)
    custom_perfume = serializers.SerializerMethodField()

    def get_user_reviews(self, obj):
        return ReviewSerializer(obj.user_reviews.all().order_by('-created_at'), many=True).data

    def get_custom_perfume(self, obj):
        return CustomPerfumeSerializer(obj.custom_perfume.all().order_by('-created_at'), many=True).data

    class Meta:
        model = User
        fields = "__all__"

class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=("username", "password", "phone_number", "email")

