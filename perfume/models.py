from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Perfume(models.Model):
    title = models.CharField(max_length=100)

    
class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_reviews")
    # perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE, related_name="perfume_reviews")
    good_content = models.TextField()
    bad_content = models.TextField()
    grade = models.IntegerField(default=5, null=False, blank=True)
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.good_content, self.bad_content)