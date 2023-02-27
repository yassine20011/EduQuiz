from django.contrib import admin

# Register your models here.
from .models import Profile, DataRelatedToUser, Quiz, Question, Answer, StudentAnswer, QuizTaker, ClassRoom, GroupQuiz
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import user_passes_test



class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by')
    list_filter = ('name', 'created_by')
    search_fields = ('name', 'created_by__username')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if request.user.is_superuser:
            form.base_fields['created_by'].disabled = True
            form.base_fields['created_by'].initial = request.user
            form.base_fields['users'].required = False
        return form
    
admin.site.register(ClassRoom, ClassRoomAdmin)


admin.site.unregister(User)
class CustomUserAdmin(UserAdmin):
    
    readonly_fields = ('date_joined', 'last_login', 'user_permissions', 'groups')
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active')    
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser:
            form.base_fields['is_staff'].disabled = True
            form.base_fields['is_superuser'].disabled = True
            
        return form

admin.site.register(User, CustomUserAdmin)







class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'isTeacher')
    list_filter = ( 'user', 'isTeacher')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('user','avatar')
    
   
    
admin.site.register(Profile, ProfileAdmin)







class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)


        form.base_fields['profile'].disabled = True
        if request.user.is_staff and request.user.profile.isTeacher:
            form.base_fields['profile'].initial = request.user
            
        return form

admin.site.register(Quiz, QuizAdmin)



class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    
admin.site.register(Question, QuestionAdmin)


    
class QuizTakerAdmin(admin.ModelAdmin):
    list_display = ('student',  'quiz', 'has_passed_quiz', 'score', 'bolong_to_group')
    list_filter = ('student', 'quiz', 'has_passed_quiz', 'score', 'bolong_to_group')
    search_fields = ('student__user__username', 'quiz__title', 'score')
    
admin.site.register(QuizTaker, QuizTakerAdmin)


class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'profile')
    list_filter = ('quiz', 'profile')
    search_fields = ('quiz__title', 'profile__user__username')
    
admin.site.register(StudentAnswer, StudentAnswerAdmin)