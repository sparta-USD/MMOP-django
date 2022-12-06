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
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from django.contrib.auth.forms import PasswordResetForm

from django.urls import reverse_lazy
from django.shortcuts import render

# 비밀번호 재설정
import re
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation

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
    # 전송된 이메일 내용
    html_email_template_name = "password_reset_email.html"
    # 전송될 이메일 제목 
    subject_template_name = "password_reset_subject.txt"
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

# 비밀번호 재설정
# SetPasswordForm 커스터마이징
class UserSetPasswordForm(forms.Form):
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
        "password_necessary":_("비밀번호는 8-20자이며 최소 하나 이상의 대/소문자, 숫자, 특수문자가 필요합니다."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        correct_password = re.compile("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,21}$")
        password_input = correct_password.match(self.cleaned_data.get("new_password1", ""))
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
            # 정규표현식
            if password_input == None:
                raise ValidationError(
                    self.error_messages["password_necessary"],
                    code="password_necessary",
                )

        password_validation.validate_password(password2, self.user)
        return password2
    
    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "password_reset_confirm.html"
    form_class = UserSetPasswordForm

# 비밀번호 재설정 완료
class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "password_reset_complete.html"