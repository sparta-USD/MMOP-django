from rest_framework import serializers
from .models import Perfume
from perfume.models import Review
from custom_perfume.serializers import NoteSerializer

class PerfumeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfume
        fields = '__all__'
        
# review
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    perfume = PerfumeBaseSerializer()

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

class SurveySerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        reviews = Review.objects.filter(
            user = validated_data['user'], 
            perfume=validated_data['perfume']
        )
        if reviews: # 해당 리뷰 남긴 향수에 대해서 설문조사를 남긴 경우
            instance = reviews[0]
            instance.survey = validated_data.get('survey',instance.survey)
            instance.save()
            return instance
        else: # 해당 새로운 향수에 대해서 설문조사를 남긴 경우
            return Review.objects.create(**validated_data)

    class Meta:
        model = Review
        fields = ('id','user','perfume','grade','survey')


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