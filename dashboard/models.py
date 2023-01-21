from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from .formatChecker import ContentTypeRestrictedFileField




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio = models.TextField(blank=True, max_length=150)
    avatar = ContentTypeRestrictedFileField(max_upload_size=10485760, null=True, verbose_name="",default='default.jpg', blank= True, content_types=['image/png', 'image/jpeg'])
    isTeacher = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

class Quiz(models.Model):
    question = models.CharField(max_length=150, null=True)
    a = models.BooleanField(default=False)
    b = models.BooleanField(default=False)
    c = models.BooleanField(default=False)
    d = models.BooleanField(default=False)
    

class DataRelatedToUser(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    device_name = models.CharField(max_length=150, null=True, default='Unknown')
    http_user_agent = models.CharField(max_length=150, null=True)
    ip_address = models.GenericIPAddressField(max_length=30, null=True)
    geoip = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(null=True)
    
    def __str__(self):
        return f'{self.ip_address}'
