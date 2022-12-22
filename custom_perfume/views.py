from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .models import *
from .serializers import *
from django.db.models import Count

# Create your views here.
class CustomPerfumeView(APIView):
    def get (self, request):
        custom_perfume = CustomPerfume.objects.all().order_by('-created_at')
        serializer = CustomPerfumeSerializer(custom_perfume, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomPerfumeCreateView(APIView):
    def get (self, request):
        notes = Note.objects.all()[:974] # Note id=973까지가 커스텀 향수 제작시 사용되는 향
        
        # cnt는 현재 향이 쓰이고 있는지 확인하는 변수
        custom_notes = []
        for note in notes:
            cnt = 0
            cnt += note.perfumes_top.aggregate(cnt=Count('id'))["cnt"]
            cnt += note.perfumes_none.aggregate(cnt=Count('id'))["cnt"]
            cnt += note.perfumes_heart.aggregate(cnt=Count('id'))["cnt"]
            cnt += note.perfumes_base.aggregate(cnt=Count('id'))["cnt"]
            if cnt > 1:
                custom_notes.append(note)
        packages = Package.objects.all()
        note_category = NoteCategory.objects.all()
        package_category = PackageCategory.objects.all()
        notes_serializer = NoteSerializer(custom_notes, many=True)
        packages_serializer = PackageSerializer(packages, many=True)
        note_category_serializer = NoteCategorySerializer(note_category, many=True)
        package_category_serializer = PackageCategorySerializer(package_category, many=True)
        return Response({'notes':notes_serializer.data, 'packages':packages_serializer.data, 'note_category':note_category_serializer.data, 'package_category':package_category_serializer.data}, status=status.HTTP_200_OK)

    def post (self, request):
        request_user = request.user     # 로그인한 유저
        # request_user = get_user_model().objects.get(id=1)   # 로그인한 유저(임시 1번 유저)
        serializer = CustomPerfumeCreateSerializer(data=request.data)
        request.data.update({'creator': request_user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomPerfumeDetailView(APIView):
    def get(self, request, custom_perfume_id):
        custom_perfume = get_object_or_404(CustomPerfume, id=custom_perfume_id)
        serializer = CustomPerfumeSerializer(custom_perfume)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete (self, request, custom_perfume_id):
        request_user = request.user     # 로그인한 유저
        # request_user = get_user_model().objects.get(id=1)   # 로그인한 유저(임시 1번 유저)
        custom_perfume = get_object_or_404(CustomPerfume, id=custom_perfume_id)
        if request_user == custom_perfume.creator :
            custom_perfume.delete()
            return Response({"messages": "커스텀한 향수가 삭제 되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)