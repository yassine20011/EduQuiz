from django.contrib.auth.forms import PasswordResetForm
from statistics import mode
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .forms import UpdateUserForm, UpdateAvatarBio, MadeQuizForm, MadeQuestionForm, MadeAnswerForm, QuestionFormSet
from .models import DataRelatedToUser, Profile
from django.contrib.auth import logout
from django.views.generic.list import ListView
from .models import Quiz, Question, Answer
import json
from django.shortcuts import get_object_or_404
import pandas as pd

def dashboard(request):
    return render(request, 'dashboard.html',)


# Profile view
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateAvatarBio(
            request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('profile')
        messages.success(request, 'Your profile not updated')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateAvatarBio(instance=request.user.profile)
    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})


def control(request):
    return render(request, 'control.html')


def create_quiz(request):  # sourcery skip: extract-method
    
    quiz_form = MadeQuizForm(request.POST or None, request.FILES or None)
    quizzes = Quiz.objects.all()
    
    
    if request.method == 'POST':
        quiz_form = MadeQuizForm(request.POST, request.FILES)
        if quiz_form.is_valid():
            
            quiz = quiz_form.save(commit=False)
            quiz.upload_quiz = request.FILES['upload_quiz']
            quiz.profile = request.user
            quiz.save()
            
            quiz = quiz_form.cleaned_data['title']
            quiz = Quiz.objects.get(title=quiz)
            
            
            if quiz.upload_quiz.name.endswith('.xlsx'):
                df = pd.read_excel(quiz.upload_quiz , engine='openpyxl')
            elif quiz.upload_quiz.name.endswith('.csv'):
                df = pd.read_csv(quiz.upload_quiz)
                
            try:
                list_of_dict = df.to_dict('records')
            except UnboundLocalError:
                messages.error(request, "Please upload a csv or xlsx file")
                return redirect('create_quiz')
            
            
            for item in list_of_dict:
                for key ,value in item.items():
                    if key == 'question':
                        question = Question.objects.filter(quiz=quiz)
                        question = question.create(question=value, quiz=quiz)
                    if key in ['a', 'b', 'c', 'd']:
                        true = '-v' in str(value)
                        value = str(value).replace('-v', '')
                        answer = Answer.objects.filter(question=question)
                        answer.create(answer=value, question=question, is_correct=true)
            
            
            messages.success(request, "Quiz created successfully")
            return redirect('create_quiz')
        
        
        
        else:
            messages.error(request, "The title is already taken")

    return render(request, 'create_quiz.html', {'quiz_form': quiz_form, 'quizzes': quizzes})



def delete_quiz(request, quiz_title):
    quiz = Quiz.objects.get(title=quiz_title)
    quiz.delete()
    return redirect('create_quiz')


def create_questions(request, quiz_title):
    quiz = Quiz.objects.get(title=quiz_title)
    question = Question.objects.filter(quiz=quiz)
    form = MadeQuestionForm(request.POST or None)

    if request.method == 'POST':
        if not form.is_valid():
            return render(request, 'question_form.html', {'form': form})

        form = form.save(commit=False)
        form.quiz = quiz
        form.save()
        HttpResponse('success')

    return render(request, 'create_question.html', {
        "form": form,
        "quiz": quiz,
        "question": question,
    })


def create_question_form(request):
    form = MadeQuestionForm()
    context = {"form": form}
    return render(request, 'question_form.html', context)

def view_quiz(request, quiz_title):
    quiz = Quiz.objects.get(title=quiz_title)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quiz_preview.html', {'quiz': quiz, 'questions': questions})


def settings(request):
    return render(request, 'settings.html')


class SecurityQuery(ListView):
    model = DataRelatedToUser
    context_object_name = "ip_adresse"
    template_name = 'security.html'

    def get_queryset(self):  # sourcery skip: inline-immediately-returned-variable
        profile = Profile.objects.get(user=self.request.user)
        ip_addresses = DataRelatedToUser.objects.filter(
            profile=profile).order_by('-date')
        return ip_addresses

    def get_context_data(self, **kwargs):
        context = super(SecurityQuery, self).get_context_data(**kwargs)
        context['change_password'] = PasswordResetForm(self.request.POST)
        return context


def logout_request(request):
    logout(request)
    return redirect("home")


# if len(request.FILES) != 0:
                