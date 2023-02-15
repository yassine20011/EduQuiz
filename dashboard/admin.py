from django.contrib import admin

# Register your models here.
from .models import Profile, DataRelatedToUser, Quiz, Question, Answer, StudentAnswer, QuizTaker


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


    
class QuizTakerAdmin(admin.ModelAdmin):
    list_display = ('student',  'has_passed_quiz')
    list_filter = ('has_passed_quiz', 'student')
    search_fields = ('student__username', 'quiz__title')
    
admin.site.register(QuizTaker, QuizTakerAdmin)


class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'profile')
    list_filter = ('quiz', 'profile')
    search_fields = ('quiz__title', 'profile__user__username')
    
admin.site.register(StudentAnswer, StudentAnswerAdmin)