from django.db import models
from django.contrib.auth import get_user_model
from custom_perfume.models import Note

# Create your models here.
class Perfume(models.Model):
    origin_id = models.IntegerField()
    image = models.CharField(max_length=256,null=True, blank=True)
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=100,null=True, blank=True)
    gender = models.CharField(max_length=5,null=True, blank=True)
    price = models.FloatField(default=0)
    launch_date = models.DateField(null=True, blank=True)
    top_notes = models.ManyToManyField(to=Note, related_name="perfumes_top", blank=True)
    heart_notes = models.ManyToManyField(to=Note, related_name="perfumes_heart", blank=True)
    base_notes = models.ManyToManyField(to=Note, related_name="perfumes_base", blank=True)
    none_notes = models.ManyToManyField(to=Note, related_name="perfumes_none", blank=True)

    class Meta:
        db_table = "perfume"
        verbose_name = '향수'  # 단수형 
        verbose_name_plural = '향수 제품'  # 복수형
        ordering = ['-launch_date','brand','title']

    def __str__(self):
        return self.title

    
class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_reviews")
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE, related_name="perfume_reviews")
    good_content = models.TextField()
    bad_content = models.TextField()
    grade = models.IntegerField(default=5, null=False, blank=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.good_content, self.bad_content)

