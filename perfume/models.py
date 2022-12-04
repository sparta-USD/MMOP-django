from django.db import models

# Create your models here.
class Perfume(models.Model):
    origin_id = models.IntegerField()
    image = models.CharField(max_length=256,null=True, blank=True)
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=100,null=True, blank=True)
    gender = models.CharField(max_length=5,null=True, blank=True)
    price = models.FloatField(default=0)
    launch_date = models.DateField(null=True, blank=True)
    top_notes = models.TextField(null=True, blank=True)
    heart_notes = models.TextField(null=True, blank=True)
    base_notes = models.TextField(null=True, blank=True)
    none_notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "perfume"
        verbose_name = '향수'  # 단수형 
        verbose_name_plural = '향수 제품'  # 복수형
        ordering = ['-launch_date','brand','title']

    def __str__(self):
        return self.title