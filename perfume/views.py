from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .models import Perfume, Review
from .serializers import PerfumeSerializer,ReviewSerializer,ReviewCreateSerializer,ReviewUpdateSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Max
import random

class PerfumeView(APIView):
    def get(self, request):
        all_perfume = Perfume.objects.all().order_by("-launch_date","brand","title")
        serializer = PerfumeSerializer(all_perfume, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PerfumeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PerfumeDetailView(APIView):
    def get(self, request, id):
        target_perfume = get_object_or_404(Perfume ,id=id)
        serializer = PerfumeSerializer(target_perfume)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        target_perfume = get_object_or_404(Perfume ,id=id)
        serializer = PerfumeSerializer(target_perfume, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        target_perfume = get_object_or_404(Perfume ,id=id)
        target_perfume.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PerfumeRandomView(APIView):
    def get(self, request):
        limit = int(request.data.get("limit",20)) # 데이터 없으면 limit = 20

        max_id = Perfume.objects.aggregate(max_id=Max('id'))['max_id']
        perfume_random_list = []
        while len(perfume_random_list) < limit: # 무조건 limit 갯수만큼 random 추출
            random_index = random.randint(1, max_id)
            perfume = Perfume.objects.get(id=random_index)
            if perfume:
                serializer = PerfumeSerializer(perfume)
                perfume_random_list.append(serializer.data)
        return Response(perfume_random_list, status=status.HTTP_200_OK)

class ReviewView(APIView):
    # 리뷰 목록 조회하기
    def get(self, request, perfume_id): 
        reviews = Review.objects.all().order_by('-created_at') # 리뷰 생성 순으로 조회
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # 리뷰 작성하기
    def post(self, request, perfume_id):
        request_user = request.user
        request.data.update({'user': request_user.id, 'perfume':perfume_id})
        
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class ReviewDetailView(APIView):
    # 리뷰 수정하기
    def put(self, request, review_id): 
        review = get_object_or_404(Review, id=review_id)
        # request_user = request.user   # 로그인한 유저
        request_user = get_user_model().objects.get(id=1)   # 로그인한 유저(임시 1번 유저)
        serializer = ReviewUpdateSerializer(review, data=request.data)
        if request_user == review.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

    # 리뷰 삭제하기
    def delete(self, request, review_id): 
        review = get_object_or_404(Review, id=review_id)
        # request_user = request.user   # 로그인한 유저
        request_user = get_user_model().objects.get(id=1)   # 로그인한 유저(임시 1번 유저)
        if request_user == review.user :
            review.delete()
            return Response({"messages": "삭제 되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else: 
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
