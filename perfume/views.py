from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .models import Perfume, Review
from .serializers import PerfumeSerializer,ReviewSerializer,ReviewCreateSerializer,ReviewUpdateSerializer,SurveySerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Max
from .recommend import recommend
import random
from rest_framework.permissions import AllowAny
from .permission import IsAuthenticated, IsAdminOrReadOnly, IsOwnerIsAdminOrReadOnly

class PerfumeView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        all_perfume = Perfume.objects.all().order_by("-likes", "-launch_date","brand","title")
        serializer = PerfumeSerializer(all_perfume, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PerfumeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PerfumeDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]
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
    permission_classes = [AllowAny]
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

class PerfumeRecommendView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        target_perfume_list = Review.objects.filter(user=request.user.id, grade__range=(4.0,5.0)).values('perfume') # 평점 4.0이상으로 내가 작성한 리뷰
        target_perfume_id = [x['perfume'] for x in target_perfume_list] # 리뷰의 pefume_id 리스트
        limit = 24

        if(target_perfume_id):
            # 추천 시스템
            recommend_index_list = recommend(target_perfume_id,limit)
            recommend_perfume = list(Perfume.objects.filter(id__in=recommend_index_list))
            recommend_perfume = sorted(recommend_perfume, key=lambda x:recommend_index_list.index(x.id))  #recommend_index_list의 순서대로 결과값 정렬
            serializer = PerfumeSerializer(recommend_perfume, many=True)
        else:
            # 추천 내용이 없으면 전체목록 보여주기
            all_perfume = Perfume.objects.all().order_by("-likes","-launch_date","brand","title")[:limit]
            serializer = PerfumeSerializer(all_perfume, many=True)
           
        return Response(serializer.data, status=status.HTTP_200_OK)

class PerfumeProductRecommendView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, perfume_id):
        target_perfume = get_object_or_404(Perfume ,id=perfume_id)
        target_perfume_id = [target_perfume.id]
        limit = 12
        # 추천 시스템
        recommend_index_list = recommend(target_perfume_id,limit)
        recommend_perfume = list(Perfume.objects.filter(id__in=recommend_index_list))
        recommend_perfume = sorted(recommend_perfume, key=lambda x:recommend_index_list.index(x.id))  #recommend_index_list의 순서대로 결과값 정렬
        serializer = PerfumeSerializer(recommend_perfume, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SurveyView(APIView):
    permission_classes = [IsAuthenticated]
    # 내가 작성한 향수추천 설문조사 조회
    def get(self,request):
        request_user = request.user
        
        reviews = Review.objects.filter(
            user=request_user, 
            survey=True
        )
        serializer = SurveySerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 향수 추천을 위한 설문조사 작성하기
    def post(self, request):    
        request_user = request.user

        survey_list = request.data['perfume_id']
        survey_perfumes = Perfume.objects.filter(id__in=survey_list).all()
        survey_dict=[]
        for perfume in survey_perfumes:
            review = {
                'user': request_user.id,
                'perfume': perfume.id,
                'survey':True
            }
            survey_dict.append(review)
        serializer = SurveySerializer(data=survey_dict, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewView(APIView):
    permission_classes = [IsOwnerIsAdminOrReadOnly]
    # 리뷰 목록 조회하기
    def get(self, request, perfume_id): 
        reviews = Review.objects.all().order_by('-created_at') # 리뷰 생성 순으로 조회
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # 리뷰 작성하기
    def post(self, request, perfume_id):
        request_user = request.user
        data = request.data.dict()
        data.update({'user': request_user.id, 'perfume':perfume_id})
        
        # user가 리뷰 작성 시 perfume_id 당 1개씩 작성 제한
        perfume = Perfume.objects.get(id=perfume_id)
        reviews = perfume.perfume_reviews.all() # 역참조 : related_name="perfume_reviews"
        for review in reviews:
            if request_user == review.user:
                return Response({"message": "이미 리뷰를 작성하였습니다!"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ReviewCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        
class ReviewDetailView(APIView):
    permission_classes = [IsOwnerIsAdminOrReadOnly]
    def get(self, request, perfume_id): 
        reviews = Review.objects.all().order_by('-created_at') # 리뷰 생성 순으로 조회
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 리뷰 수정하기
    def put(self, request, review_id): 
        review = get_object_or_404(Review, id=review_id)
        request_user = request.user 
        if request_user == review.user:
            serializer = ReviewUpdateSerializer(review, data=request.data)
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
        request_user = request.user   
        if request_user == review.user :
            review.delete()
            return Response({"messages": "리뷰가 삭제 되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else: 
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
        

# 찜하기
class LikeView(APIView):
    permission_classes = [IsOwnerIsAdminOrReadOnly]
    def post(self, request, perfume_id):
        perfume = get_object_or_404(Perfume, id=perfume_id)
        request_user = request.user  
        if request_user in perfume.likes.all():
            perfume.likes.remove(request_user)
            return Response({"messages": "찜 목록에서 삭제되었습니다!"}, status=status.HTTP_200_OK)
        else:
            perfume.likes.add(request_user)
            return Response({"messages": "찜 목록에서 추가되었습니다!"}, status=status.HTTP_200_OK)