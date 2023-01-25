from django.contrib import admin

# Register your models here.
from .models import Profile, DataRelatedToUser, Quiz, Question, Answer


admin.site.register(Profile)
admin.site.register(DataRelatedToUser)




class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Quiz, QuizAdmin)

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    
admin.site.register(Question, QuestionAdmin)

