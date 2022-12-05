from django.urls import path
from . import views
urlpatterns = [
    path("", views.PerfumeView.as_view(), name="perfume_view"),
    path("<int:id>/", views.PerfumeDetailView.as_view(), name="perfume_detail_view"),

    # <int:perfume_id>/ 추가필요!!
    path('reviews/', views.ReviewView.as_view(), name='review_view'),
    path('reviews/<int:review_id>/', views.ReviewDetailView.as_view(), name='review_detail_view'),
]
