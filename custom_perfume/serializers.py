from rest_framework import serializers
from .models import *


class PackageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageCategory
        fields = '__all__'
        
class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'
        
class NoteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteCategory
        fields = '__all__'
        
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        
class CustomPerfumeSerializer(serializers.ModelSerializer):
    note01 = NoteSerializer()
    note02 = NoteSerializer()
    note03 = NoteSerializer()
    package = PackageSerializer()
    creator_username = serializers.SerializerMethodField()

    class Meta:
        model = CustomPerfume
        fields = '__all__'

    def get_creator_username(self, obj):
        return obj.creator.username
