from django import forms
from django.contrib.auth.models import User
from .models import Profile, DataRelatedToUser, Quiz, Question, Answer, StudentAnswer, QuizTaker, ClassRoom, GroupQuiz
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
        attrs={'class': 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400'}))
    first_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(
        attrs={'class': 'mb-6 bg-gray-100 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 cursor-not-allowed dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500', 'disabled': 'disabled'}))
    last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(
        attrs={'class': 'mb-6 bg-gray-100 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 cursor-not-allowed dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500', 'disabled': 'disabled'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={'class': 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400'}))
    

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UpdateAvatarBio(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'block w-full mb-5 text-xs text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'}))
  

    class Meta:
        model = Profile
        fields = ['avatar']




class MadeQuizForm(forms.ModelForm):
    CHOICES = [(group.id, group.name) for group in ClassRoom.objects.all()]
    
    title = forms.CharField(max_length=255, required=True, widget=forms.TextInput(
        attrs={'class': 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400'}), label='Quiz Title(Make it short and descriptive e.g. "Algebra 1 Quiz 1")')
    start_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label='Start Date', required=True)
    end_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    group = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), widget=forms.Select(attrs={'class': 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400'}), required=True, label='Select Group')
    upload_quiz = forms.FileField(widget=forms.FileInput(
        attrs={'class': 'block w-full mb-5 text-xs text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'}), required=True,  label='Upload Quiz(.csv or .xlsx)')
    
    
    class Meta:
        model = Quiz
        fields = ['title', 'start_at', 'end_at', 'group', 'upload_quiz']
        
   
        
class MadeQuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['question']


class MadeAnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['answer', 'is_correct']



class StudentAnswerForm(forms.ModelForm):

    class Meta:
        model = StudentAnswer
        fields = ['answer']