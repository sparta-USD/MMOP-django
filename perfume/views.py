from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .models import Perfume
from .serializers import PerfumeSerializer

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
        target_parfume = get_object_or_404(Perfume ,id=id)
        serializer = PerfumeSerializer(target_parfume)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        target_parfume = get_object_or_404(Perfume ,id=id)
        serializer = PerfumeSerializer(target_parfume, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        target_parfume = get_object_or_404(Perfume ,id=id)
        target_parfume.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)