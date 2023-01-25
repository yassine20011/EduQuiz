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


    

class DataRelatedToUser(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    device_name = models.CharField(max_length=150, null=True, default='Unknown')
    http_user_agent = models.CharField(max_length=150, null=True)
    ip_address = models.GenericIPAddressField(max_length=30, null=True)
    geoip = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(null=True)
    
    def __str__(self):
        return f'{self.ip_address}'


class Quiz(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, unique=True, null=True)
    start_at = models.DateTimeField(null=True)
    end_at = models.DateTimeField()
    upload_quiz = ContentTypeRestrictedFileField(max_upload_size=10485760, null=True, verbose_name="", blank= True, content_types=['image/csv', 'image/xlsx'])
    
    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=500, null=True)
    
    
    def __str__(self):
        return self.question

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=255, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer