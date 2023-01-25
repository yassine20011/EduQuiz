from django import forms
from django.contrib.auth.models import User
from .models import Profile, DataRelatedToUser, Quiz, Question, Answer
from django.forms.models import inlineformset_factory


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
        attrs={'class': 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400'}))
    first_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(
        attrs={'class': 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400'}))
    last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(
        attrs={'class': 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={'class': 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400'}))
    

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UpdateAvatarBio(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'block w-full mb-5 text-xs text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'}))
    bio = forms.CharField(max_length=150, required=False, widget=forms.TextInput(
        attrs={'class': 'bg-white dark:bg-gray-800'}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class MadeQuizForm(forms.ModelForm):
    title = forms.CharField(max_length=255, required=True, widget=forms.TextInput(
        attrs={'class': 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400'}))
    upload_quiz = forms.FileField(widget=forms.FileInput(
        attrs={'class': 'block w-full mb-5 text-xs text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'}), required=True,  label='Upload Quiz(.csv or .xlsx)')
    
    
    
    class Meta:
        model = Quiz
        fields = ['title', 'start_at', 'end_at']


class MadeQuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['question']


class MadeAnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['answer', 'is_correct']


QuestionFormSet = inlineformset_factory(Quiz, Question, form=MadeQuestionForm, extra=2, can_delete=True)