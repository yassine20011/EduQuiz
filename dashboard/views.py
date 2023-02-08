from django.contrib.auth.forms import PasswordResetForm
from statistics import mode
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import UpdateUserForm, UpdateAvatarBio, MadeQuizForm, MadeQuestionForm
from .models import DataRelatedToUser, Profile, Quiz, Question, Answer, StudentAnswer, QuizTaker
from django.contrib.auth import logout
from django.views.generic.list import ListView
import pandas as pd
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
import json
from collections import defaultdict
from django.contrib.auth.models import Group


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


@user_passes_test(lambda u: u.is_staff)
def create_quiz(request):

    quiz_form = MadeQuizForm(request.POST or None, request.FILES or None)
    quizzes = Quiz.objects.all()

    if request.method == 'POST':
        # this is the form that is submitted
        quiz_form = MadeQuizForm(request.POST, request.FILES)

        if quiz_form.is_valid():  # check if the form is valid

            # calulate the time limit using start and end time
            dt = quiz_form.cleaned_data['end_at'] - \
                quiz_form.cleaned_data['start_at']

            # convert the time to minutes
            dt = dt.total_seconds() / 60

            # commit = False means that the form is not saved yet or there is some null values
            quiz = quiz_form.save(commit=False)
            # get the file from the form
            quiz.upload_quiz = request.FILES['upload_quiz']
            quiz.profile = request.user
            quiz.time_limit = dt
            quiz.save()

            # get the title of the quiz
            quiz = quiz_form.cleaned_data['title']
            quiz = Quiz.objects.get(title=quiz)

            # read the file and convert it to a list of dictionaries
            if quiz.upload_quiz.name.endswith('.xlsx'):
                df = pd.read_excel(quiz.upload_quiz, engine='openpyxl')
            elif quiz.upload_quiz.name.endswith('.csv'):
                df = pd.read_csv(quiz.upload_quiz)

            try:
                list_of_dict = df.to_dict('records')
            except UnboundLocalError:
                messages.error(request, "Please upload a csv or xlsx file")
                return redirect('create_quiz')

            # create questions and answers
            for item in list_of_dict:
                for key, value in item.items():
                    if key.lower() == 'question':
                        question = Question.objects.filter(quiz=quiz)
                        question = question.create(question=value, quiz=quiz)
                    if key in ['a', 'b', 'c', 'd']:
                        true = '-v' in str(value)
                        value = str(value).replace('-v', '')
                        answer = Answer.objects.filter(question=question)
                        answer.create(
                            answer=value, question=question, is_correct=true)

            messages.success(request, "Quiz created successfully")
            return redirect('create_quiz')

        else:
            messages.error(request, "The title is already taken")

    return render(request, 'create_quiz.html', {'quiz_form': quiz_form, 'quizzes': quizzes})


@user_passes_test(lambda u: u.is_staff)
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


@user_passes_test(lambda u: u.is_staff)
def view_quiz(request, quiz_title):
    quiz = Quiz.objects.get(title=quiz_title)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quiz_preview.html', {'quiz': quiz, 'questions': questions})


def available_quizzes(request):
    quizzes = Quiz.objects.all()

    return render(request, 'available_quiz.html', {'quizzes': quizzes})


def take_quiz(request, quiz_title):  # sourcery skip: remove-redundant-pass
    quiz = Quiz.objects.get(title=quiz_title)
    
   
    
    
    if request.method == 'POST':
        # It's a dictionary of the form data.
        ajaxData = {
            key: value
            for key, value in request.POST.lists()
            if key != 'csrfmiddlewaretoken'
        }

        list_of_dict = []
        for i in range(len(ajaxData) // 2):
            new_dict = {'question_id': ajaxData[f'values[{int(i)}][question_id]'],
                        'answer_id': ajaxData[f'values[{int(i)}][answer_id][]']}
            list_of_dict.append(new_dict)
  
        
        for item in list_of_dict:
            question = Question.objects.get(id=int(item['question_id'][0]))
            studentAnswer = StudentAnswer.objects.create(profile=request.user, quiz=quiz, question=question)
            studentAnswer.answer.add(*item['answer_id'])
            studentAnswer.save()
        
       
        QuizTaker.objects.create(student=request.user, has_passed_quiz=True, quiz=quiz)
        return HttpResponseRedirect('/')
     
    quiz = Quiz.objects.get(title=quiz_title)
    end = quiz.end_at.strftime("%Y-%m-%d %H:%M:%S")
    random_questions = Question.objects.filter(quiz=quiz).order_by('?')
    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': random_questions, 'end': end})


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
