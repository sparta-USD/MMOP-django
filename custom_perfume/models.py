import os
from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
def upload_to_custom_perfume_logo(instance, filename):
    upload_to = f'custom_perfume_logo/'
    ext = filename.split('.')[-1]
    uuid = uuid4().hex
    filename = '{}.{}'.format(uuid, ext)
    return os.path.join(upload_to, filename)

class PackageCategory(models.Model):
    name = models.CharField(max_length=100)

class Package(models.Model):
    name = models.CharField(max_length=100)
    image = models.TextField()
    package_category = models.ForeignKey(PackageCategory, on_delete=models.CASCADE)

class NoteCategory(models.Model):
    name = models.CharField(max_length=100)
    kor_name = models.CharField(max_length=100)

class Note(models.Model):
    name = models.CharField(max_length=100)
    kor_name = models.CharField(max_length=100)
    image = models.TextField()
    note_category = models.ForeignKey(NoteCategory, on_delete=models.CASCADE, related_name='note01', null=True, blank=True)
    # tag = models.TextField(null=True, blank=True)
    
class CustomPerfume(models.Model):
    title = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=upload_to_custom_perfume_logo, max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='custom_perfume')
    note01 = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='note01', null=True, blank=True)
    note02 = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='note02', null=True, blank=True)
    note03 = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='note03', null=True, blank=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='package')
    

    

