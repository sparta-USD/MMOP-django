from django.contrib import admin
from .models import Perfume
from perfume.models import Review

# Register your models here.
admin.site.register(Perfume)
admin.site.register(Review)
