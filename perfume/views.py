from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404
from perfume import serializers
from perfume.models import Review
from perfume.serializers import ReviewSerializer,ReviewCreateSerializer
from django.contrib.auth.decorators import login_required


# Create your views here.
class ReviewView(APIView):
    # 리뷰 목록 조회하기
    def get(self, request): # perfume_id 추가 필요!
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # 리뷰 작성하기
    def post(self, request):
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)