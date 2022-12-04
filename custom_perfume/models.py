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

def upload_to_note_image(instance, filename):
    upload_to = f'note_image/'
    ext = filename.split('.')[-1]
    uuid = uuid4().hex
    filename = '{}.{}'.format(uuid, ext)
    return os.path.join(upload_to, filename)

def upload_to_package_image(instance, filename):
    upload_to = f'package_image/'
    ext = filename.split('.')[-1]
    uuid = uuid4().hex
    filename = '{}.{}'.format(uuid, ext)
    return os.path.join(upload_to, filename)

class PackageCategory(models.Model):
    name = models.CharField(max_length=100)

class Package(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_to_package_image, max_length=255)
    package_category = models.ForeignKey(PackageCategory, on_delete=models.CASCADE)

class NoteCategory(models.Model):
    name = models.CharField(max_length=100)

class Note(models.Model):
    name = models.CharField(max_length=100)
    kor_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_to_note_image, max_length=255, null=True)
    note_category = models.ForeignKey(NoteCategory, on_delete=models.CASCADE)
    
class CustomPerfume(models.Model):
    title = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=upload_to_custom_perfume_logo, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    # creator = models.ForeignKey(모델, on_delete=models.CASCADE)
    note01 = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='note01')
    note02 = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='note02')
    note03 = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='note03')
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    

    

