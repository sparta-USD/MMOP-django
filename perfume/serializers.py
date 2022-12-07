from rest_framework import serializers
from .models import Perfume
from perfume.models import Review

# review
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
        fields = '__all__'
        
class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('good_content', 'bad_content', 'grade', 'image')


# perfume 
class PerfumeSerializer(serializers.ModelSerializer):
    perfume_reviews = ReviewSerializer(many=True)
    class Meta :
        model = Perfume
        fields = "__all__"