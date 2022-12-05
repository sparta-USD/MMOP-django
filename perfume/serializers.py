from rest_framework import serializers
from .models import Perfume
from perfume.models import Review

class PerfumeSerializer(serializers.ModelSerializer):
    class Meta :
        model = Perfume
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.username
    
    class Meta:
        model = Review
        fields = '__all__'

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("user", "good_content", "bad_content", "grade", "image")
        
class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('good_content', 'bad_content', 'grade', 'image')

