from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

# Create your views here.
class CustomPerfumeView(APIView):
    def get (self, request):
        notes = Note.objects.all()
        packages = Package.objects.all()
        note_category = NoteCategory.objects.all()
        package_category = PackageCategory.objects.all()
        notes_serializer = NoteSerializer(notes, many=True)
        packages_serializer = PackageSerializer(packages, many=True)
        note_category_serializer = NoteCategorySerializer(note_category, many=True)
        package_category_serializer = PackageCategorySerializer(package_category, many=True)
        return Response({'notes':notes_serializer.data, 'packages':packages_serializer.data, 'note_category':note_category_serializer.data, 'package_category':package_category_serializer.data}, status=status.HTTP_200_OK)

    def post (self, request):
        # request_user = request.user     # 로그인한 유저
        request_user = get_user_model().objects.get(id=1)   # 로그인한 유저(임시 1번 유저)
        serializer = CustomPerfumeSerializer(data=request.data)
        request.data.update({'creator': request_user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)