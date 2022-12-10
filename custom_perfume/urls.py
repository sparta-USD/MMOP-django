from django.urls import path
from custom_perfume import views

urlpatterns = [
    path('', views.CustomPerfumeView.as_view(), name='custom_perfume_view'),
    path('custom/', views.CustomPerfumeCreateView.as_view(), name='custom_perfume_create_view'),
    path('<int:custom_perfume_id>/', views.CustomPerfumeDeleteView.as_view(), name='custom_perfume_delete_view'),
]
