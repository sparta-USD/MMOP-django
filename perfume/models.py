import os
from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from custom_perfume.models import Note

class Brand(models.Model):
    origin_id = models.IntegerField()
    image = models.CharField(max_length=256,null=True, blank=True)
    title = models.CharField(max_length=100)
    website = models.CharField(max_length=256,null=True, blank=True)
    brand_desc = models.TextField(null=True, blank=True)
    brand_desc_ko = models.TextField(null=True, blank=True)


class Perfume(models.Model):
    origin_id = models.IntegerField()
    image = models.CharField(max_length=256,null=True, blank=True)
    title = models.CharField(max_length=256)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="brand_perfume")
    gender = models.CharField(max_length=5,null=True, blank=True)
    price = models.FloatField(default=0)
    price_unit = models.CharField(default="USD", max_length=100 ,null=True, blank=True)
    launch_date = models.DateField(null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    desc_ko = models.TextField(null=True, blank=True)
    top_notes = models.ManyToManyField(to=Note, related_name="perfumes_top", blank=True)
    heart_notes = models.ManyToManyField(to=Note, related_name="perfumes_heart", blank=True)
    base_notes = models.ManyToManyField(to=Note, related_name="perfumes_base", blank=True)
    none_notes = models.ManyToManyField(to=Note, related_name="perfumes_none", blank=True)
    likes = models.ManyToManyField(to=get_user_model(), related_name="like_perfume", blank=True)

    class Meta:
        db_table = "perfume"
        verbose_name = '향수'  # 단수형 
        verbose_name_plural = '향수 제품'  # 복수형
        ordering = ['-launch_date','brand','title']

    def __str__(self):
        return self.title
    
    # perfume의 평균 grade 구하기
    def avg_grade(self):
        reviews = self.perfume_reviews.all() # Review 역참조
        sum_grade = 0
        if reviews:
            for review in reviews:
                sum_grade += review.grade
            avg_grade = sum_grade / len(reviews)
            avg_grade = round(avg_grade, 1)
            return avg_grade
        else: # 리뷰가 없다면
            return 0
    
    
def rename_reviewimage(instance, filename):
    upload_to = f'perfume/reviewimage/'
    ext = filename.split('.')[-1]
    uuid = uuid4().hex
    filename = '{}.{}'.format(uuid, ext)
    return os.path.join(upload_to, filename)

class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_reviews")
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE, related_name="perfume_reviews")
    good_content = models.TextField(default="",blank=True)
    bad_content = models.TextField(default="",blank=True)
    grade = models.FloatField(default=5, null=False, blank=True)
    survey = models.BooleanField(default=False, blank=True)
    image = models.ImageField(upload_to=rename_reviewimage, max_length=255,  null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.good_content, self.bad_content)

