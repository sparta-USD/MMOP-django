from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from users import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('activate/<str:uidb64>/<str:token>', views.UserEmailVaildView.as_view(), name='activate'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/',views.UserPasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', views.UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', views.UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('', views.MypageView.as_view(), name='mypage'),
    path('oauth/callback/kakao/', views.KakaoSigninView.as_view(), name='kakao_callback'),
]