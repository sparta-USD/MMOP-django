from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .models import Perfume, Review, Brand
from .serializers import PerfumeSerializer,PerfumeBaseSerializer,ReviewSerializer,ReviewCreateSerializer,ReviewUpdateSerializer,SurveySerializer,DetailBrandSerializer,AllBrandSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Max,Count,Avg
from .recommend import recommend
import random
from rest_framework.permissions import AllowAny
from .permission import IsAuthenticated, IsAdminOrReadOnly, IsOwnerIsAdminOrReadOnly
from .pagination import PerfumePagination
from rest_framework.generics import GenericAPIView
from rest_framework.filters import SearchFilter,OrderingFilter

class PerfumeView(GenericAPIView):
    '''
      향수 목록 조회
      - pagination : 20개씩
      - ?search= : 향수명, 브랜드명, 향이름(영문/한글)
      - ?ordering= : 최신순, 찜많은순, 리뷰평점순, 리뷰많은순, 무작위(설문조사)
      - 기본정렬 : 브랜드명-제품명

      향수 목록 조회 결과
      {
        count: 데이터 갯수
        last: 마지막 페이지
        next: 다음 페이지
        previous: 이전 페이지
        results:{
            향수 데이터
        }
      }
    '''
    permission_classes = [IsAdminOrReadOnly]

    queryset = Perfume.objects.annotate(likes_count=Count('likes'),reviews_count=Count('perfume_reviews'),avg_reviews_grade=Avg('perfume_reviews__grade'))
    pagination_class = PerfumePagination
    serializer_class = PerfumeSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title','brand__title','top_notes__name','top_notes__kor_name','heart_notes__name','heart_notes__kor_name','base_notes__name','base_notes__kor_name','none_notes__name','none_notes__kor_name']
    ordering_fields = ['launch_date','likes_count','avg_reviews_grade','reviews_count','?'] #최신순, 찜순, 리뷰평점순, 리뷰많은순, 무작위(설문조사)
    ordering=['brand__title','title']

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page_queryset = self.paginate_queryset(queryset)
        serializer = PerfumeSerializer(page_queryset, many=True)
        result = self.get_paginated_response(data=serializer.data)
        return Response(result, status=status.HTTP_200_OK)

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

class PerfumeSimpleView(GenericAPIView):
    '''
      향수 목록 심플 조회
      - pagination : 20개씩
      - ?search= : 향수명, 브랜드명
      - 기본정렬 : 브랜드명-제품명

      향수 목록 심플 조회 결과
      {
        count: 데이터 갯수
        last: 마지막 페이지
        next: 다음 페이지
        previous: 이전 페이지
        results: 향수 데이터
      }
    '''
    permission_classes = [IsAdminOrReadOnly]

    queryset = Perfume.objects.all()
    pagination_class = PerfumePagination
    serializer_class = PerfumeBaseSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title','brand__title']
    ordering=['brand__title','title']

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page_queryset = self.paginate_queryset(queryset)
        serializer = PerfumeBaseSerializer(page_queryset, many=True)
        result = self.get_paginated_response(data=serializer.data)
        return Response(result, status=status.HTTP_200_OK)

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
            all_perfume = Perfume.objects.annotate(likes_count=Count('likes')).order_by("-likes_count", "-launch_date","brand","title")[:limit]
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


# 향수 브랜드 
class AllBrandView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        all_brand = Brand.objects.all()
        serializer = AllBrandSerializer(all_brand, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DetailBrandView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, brand_id):
        brand = get_object_or_404(Brand ,id=brand_id)
        serializer = DetailBrandSerializer(brand)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class BrandRandomView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        limit = int(request.data.get("limit",8)) # 데이터 없으면 limit = 8
        brand  = Brand.objects.all().order_by("?")[:limit]
        serializer = AllBrandSerializer(brand, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 리뷰 전체
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

        
# 리뷰 상세조회
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