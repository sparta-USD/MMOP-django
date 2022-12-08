from rest_framework import serializers
from .models import Perfume
from perfume.models import Review
from custom_perfume.serializers import NoteSerializer

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
    avg_grade = serializers.SerializerMethodField()
    #
    likes = serializers.StringRelatedField(many=True)
    likes_count = serializers.SerializerMethodField()
    #
    top_notes = NoteSerializer(many=True)
    heart_notes = NoteSerializer(many=True)
    base_notes = NoteSerializer(many=True)
    none_notes = NoteSerializer(many=True)
    
    class Meta :
        model = Perfume
        fields = "__all__"
        
    def get_avg_grade(self, obj):
        return obj.avg_grade()
    
    def get_likes_count(self, obj):
        return obj.likes.count()