from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from .formatChecker import ContentTypeRestrictedFileField
from django.contrib.auth.models import Group




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio = models.TextField(blank=True, max_length=150)
    avatar = ContentTypeRestrictedFileField(max_upload_size=10485760, null=True, verbose_name="", blank= True, content_types=['image/png', 'image/jpeg'])
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

class ClassRoom(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='teacher_group')
    name = models.CharField(max_length=255, unique=True, null=True)
    users = models.ManyToManyField(User, related_name='student_group')
    
    
    def __str__(self):
        return self.name
    
class Quiz(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, unique=True, null=True)
    start_at = models.DateTimeField(null=True)
    end_at = models.DateTimeField()
    time_limit = models.IntegerField(null=True)
    group = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True)
    is_available = models.BooleanField(default=False)
    upload_quiz = ContentTypeRestrictedFileField(max_upload_size=10485760, null=True, verbose_name="", blank= True, content_types=['text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'])
    
    class Meta:
        ordering = ['-end_at']
    
    def __str__(self):
        return self.title
    
    

class GroupQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f'{self.quiz.title} - {self.group.name}'

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=1000, null=True)
    
    
    def __str__(self):
        return self.question

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=255, null=True)
    is_correct = models.BooleanField(default=False)


    class Meta:
        ordering = ['?']
        
    def __str__(self):
        return self.answer


    
class StudentAnswer(models.Model):
    
    profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.ManyToManyField(Answer, blank=True, related_name='student_answer')
    
    
    def __str__(self):
        return f'{self.profile.username} {self.quiz.title}'
    
    
class QuizTaker(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    bolong_to_group = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True)
    has_passed_quiz = models.BooleanField(default=False)
    score = models.IntegerField(null=True)
    
    class Meta:
        unique_together = ['student', 'quiz']
    
    def __str__(self):
        return f'{self.student.username} {self.quiz.title}'



