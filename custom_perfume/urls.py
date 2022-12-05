from django.urls import path
from custom_perfume import views

urlpatterns = [
    path('', views.CustomPerfumeView.as_view(), name='custom_perfume_view'),
    
]
