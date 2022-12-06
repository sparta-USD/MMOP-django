from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from users import views


urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.MypageView.as_view(), name='mypage'),
]