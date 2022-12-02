import os
from uuid import uuid4
from django.db import models


# Create your models here.
def upload_to_custom_perfume_logo(instance, filename):
    upload_to = f'custom_perfume_logo/'
    ext = filename.split('.')[-1]
    uuid = uuid4().hex
    filename = '{}.{}'.format(uuid, ext)
    return os.path.join(upload_to, filename)


class Perfume(models.Model):
    title = models.CharField(max_length=100)

class CustomPerfume(models.Model):
    title = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=upload_to_custom_perfume_logo, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    # creator = models.ForeignKey(모델, on_delete=models.CASCADE)
    # note01 = models.ForeignKey(모델, on_delete=models.CASCADE)
    # note02 = models.ForeignKey(모델, on_delete=models.CASCADE)
    # note03 = models.ForeignKey(모델, on_delete=models.CASCADE)
    # package = models.ForeignKey(모델, on_delete=models.CASCADE)

