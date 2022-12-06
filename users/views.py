from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import get_object_or_404

from users.serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer, MypageSerializer, ProfileEditSerializer
    )
from users.models import User

# 메일링
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView

from django.contrib.auth.forms import PasswordResetForm

from django.urls import reverse_lazy
from django.shortcuts import render

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SigninView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MypageView(APIView):
    def get(self, request):
        profile = get_object_or_404(User, username=request.user.username)
        serializer = MypageSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = get_object_or_404(User, username=request.user.username)
        serializer = ProfileEditSerializer(profile, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 비밀번호 초기화 메일보내기
class UserPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm
    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'password_reset_done_fail.html')

# 메일 전송 여부 확인            
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html' 