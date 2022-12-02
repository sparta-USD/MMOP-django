from django.urls import path
from perfume import views

urlpatterns = [
    # <int:perfume_id>/ 추가필요!!
    path('reviews/', views.ReviewView.as_view(), name='review_view'),
]
