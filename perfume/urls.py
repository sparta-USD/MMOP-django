from django.urls import path
from . import views
urlpatterns = [
    path("", views.PerfumeView.as_view(), name="perfume_view"),
    path("<int:id>/", views.PerfumeDetailView.as_view(), name="perfume_detail_view"),
    path("random/", views.PerfumeRandomView.as_view(), name="perfume_random_view"),
    path("recommend/", views.PerfumeRecommendView.as_view(), name="perfume_recommend_view"),

    path('<int:perfume_id>/reviews/', views.ReviewView.as_view(), name='review_view'),
    path('reviews/<int:review_id>/', views.ReviewDetailView.as_view(), name='review_detail_view'),
    path('<int:perfume_id>/like/', views.LikeView.as_view(), name="like_view"),
]
