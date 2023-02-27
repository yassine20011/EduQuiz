from django.template import RequestContext
from django.contrib.auth.forms import PasswordResetForm
from statistics import mode
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import UpdateUserForm, UpdateAvatarBio, MadeQuizForm, MadeQuestionForm
from .models import DataRelatedToUser, Profile, Quiz, Question, Answer, StudentAnswer, QuizTaker, ClassRoom, GroupQuiz
from django.contrib.auth import logout
from django.views.generic.list import ListView
import pandas as pd
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.utils import timezone
import pytz
from datetime import datetime
from django.http import JsonResponse
from django.db import IntegrityError
import maxminddb
import os
import pytz
from datetime import datetime
from staff.forms import CreateGroupForm


def dashboard(request):
    return render(request, 'dashboard.html')


def dashboard1(request):

    profile = Profile.objects.get(user=request.user)
    return render(request, 'dashboard1.html', {'profile': profile})


# Profile view
def profile(request):
    """
    If the request method is POST, then validate the user_form and profile_form, and if they are valid,
    save them and redirect to the profile page. 
    If the request method is not POST, then create a new user_form and profile_form.

    :param request: The request is an HttpRequest object. It contains metadata about the request,
    including the HTTP method
    :return: The profile.html page is being returned.
    """

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

@user_passes_test(lambda user: Profile.objects.get(user=user).isTeacher)
def create_quiz(request):
    """Create a quiz and save it to the database It takes a csv or xlsx file and creates a quiz with questions and answers."""

    
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
            quiz.group = quiz_form.cleaned_data['group']
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
            messages.error(request, "Something went wrong")

    return render(request, 'create_quiz.html', {'quiz_form': quiz_form, 'quizzes': quizzes})


@user_passes_test(lambda user: Profile.objects.get(user=user).isTeacher)
def delete_quiz(request, quiz_title):
    """
    If the user is staff, delete the quiz with the title of the quiz_title parameter

    :param request: The request object is a standard Django object that contains metadata about the
    request sent to the view
    :param quiz_title: The title of the quiz you want to delete
    :return: The correct answer
    """
    quiz = Quiz.objects.get(title=quiz_title)
    quiz.delete()
    return redirect('create_quiz')


@user_passes_test(lambda user: Profile.objects.get(user=user).isTeacher)
def view_quiz(request, quiz_title):
    """
    It takes a request and a quiz title, gets the quiz with that title, gets all the questions for that
    quiz, and then renders the quiz_preview.html template with the quiz and questions as context

    :param request: The request object is a Python object that contains metadata about the request sent
    to the server
    :param quiz_title: The title of the quiz you want to view
    :return: A list of questions
    """
    quiz = Quiz.objects.get(title=quiz_title)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quiz_preview.html', {'quiz': quiz, 'questions': questions})


def available_quizzes(request):
    """
    It takes a request, gets all the quizzes from the database, and then renders the available_quiz.html
    template, passing in the quizzes as a variable called quizzes

    :param request: The request is an HttpRequest object. It contains metadata about the request, such
    as the client’s IP address, the HTTP method, and the headers
    :return: A list of all the quizzes in the database.
    """
    now = timezone.now()
    quizzes = Quiz.objects.all().filter(group=ClassRoom.objects.filter(users=request.user).first())
    return render(request, 'available_quiz.html', {'quizzes': quizzes, 'now': now})


def results_with_details(request, quiz_title):
    """
    It takes a quiz title as an argument, gets all the student answers for that quiz, and then creates a
    dataframe with the student's full name, the question, the student's answers, and the student's grade

    :param request: the request object
    :param quiz_title: the title of the quiz
    :return: A list of dictionaries.
    """

    quiz = Quiz.objects.get(title=quiz_title)

    student_answers = StudentAnswer.objects.filter(quiz=quiz)
    data = []

    for student_answer in student_answers:
        student_full_name = student_answer.profile.get_full_name()
        student_question = student_answer.question
        student_answer_list = [str(answer)
                               for answer in student_answer.answer.all()]
        student_grade = QuizTaker.objects.get(
            student=student_answer.profile, quiz=quiz).score
        data.append({
            "Full name": student_full_name,
            "Question": student_question,
            "Student Answers": student_answer_list,
            "Grade": student_grade
        })

    df = pd.DataFrame(data)

    df.style.set_caption(f'{quiz_title} results').set_table_styles([{'selector': 'th',
                                                                     'props': [('background-color', '#F0F0F0'), ('font-size', '12pt'), ('text-align', 'center'), ('font-weight', 'bold'), ('border', '1px solid black')]},
                                                                    {'selector': 'td',
                                                                     'props': [('background-color', '#D0D0D0')]}])
    df.to_excel(f'media/{quiz_title} results_with_details.xlsx', index=False)
    return redirect(f"/media/{quiz_title} results_with_details.xlsx")


def standard_results(request, quiz_title):
    """
    It takes a quiz title, finds all the quiz takers for that quiz, and then creates a dataframe with
    the quiz taker's full name and score. It then styles the dataframe and saves it as an excel file

    :param request: the request object
    :param quiz_title: the title of the quiz
    :return: a redirect to the media folder.
    """
    quiz = Quiz.objects.get(title=quiz_title)
    quiz_takers = QuizTaker.objects.filter(quiz=quiz)
    data = [
        {
            "Full name": quiz_taker.student.get_full_name(),
            "Grade": quiz_taker.score,
        }
        for quiz_taker in quiz_takers
    ]
    df = pd.DataFrame(data)
    df.style.set_caption('Example XLSX') \
        .set_table_styles([{'selector': 'th',
                            'props': [('background-color', '#F0F0F0'), ('font-size', '12pt'), ('text-align', 'center'), ('font-weight', 'bold'), ('border', '1px solid black')]},
                           {'selector': 'td',
                          'props': [('background-color', '#D0D0D0')]}])
    df.to_excel(f'media/{quiz_title} standard_results.xlsx', index=False)
    return redirect(f'/media/{quiz_title} standard_results.xlsx')

@user_passes_test(lambda user: Profile.objects.get(user=user).isTeacher == False and not user.is_staff and not user.is_superuser)
def take_quiz(request, quiz_title):  # sourcery skip: remove-redundant-pass
    quiz = Quiz.objects.get(title=quiz_title)

    if QuizTaker.objects.filter(student=request.user, quiz=quiz).exists():
        return JsonResponse({'error': 'You have already taken this quiz'})
    elif quiz.end_at < timezone.now():
        return JsonResponse({'error': 'The quiz has ended'})
    elif Quiz.objects.filter(title=quiz_title, group=ClassRoom.objects.filter(users=request.user).first()).exists() == False:
        return JsonResponse({'error': 'You are not in this class'})
    
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
            studentAnswer = StudentAnswer.objects.create(
                profile=request.user, quiz=quiz, question=question)
            studentAnswer.answer.add(*item['answer_id'])
            studentAnswer.save()

        count = 0
        student_answers = StudentAnswer.objects.filter(quiz=quiz)
        for student_answer in student_answers:
            # Get the question that was answered
            question = student_answer.question
            question = Question.objects.get(id=question.id)
            true_answer = Answer.objects.filter(
                question=question, is_correct=True)
            true_answers_list = list(true_answer)
            # Get the answers for the question
            answers = student_answer.answer.all()
            answers_list = list(answers)
            if true_answers_list == answers_list:
                count = count + 1

        try:
            QuizTaker.objects.create(student=request.user, has_passed_quiz=True, quiz=quiz, score=count, bolong_to_group=ClassRoom.objects.filter(users=request.user).first())
        except IntegrityError:
            return JsonResponse({'error': 'You have already taken this quiz'})
        return redirect('dashboard1')

    quiz = Quiz.objects.get(title=quiz_title)
    end = quiz.end_at.strftime("%Y-%m-%d %H:%M:%S")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    random_questions = Question.objects.filter(quiz=quiz).order_by('?')
    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': random_questions, 'end': end, 'now': now})


def settings(request):
    return render(request, 'settings.html')



def join_groups(request, group_name=None):
    
    if group_name is not None:
        if ClassRoom.objects.all().filter(users=request.user).exists():
            messages.error(request, 'You are already in a group')
            return redirect('groups')
        else:
            group = ClassRoom.objects.get(name=group_name)
            group.users.add(request.user)
            group.save()
        return redirect('groups')
    
    
    groups = ClassRoom.objects.all()
    return render(request, 'groups.html', {'groups': groups})


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


def handler404(request, exception=None):
    return render(request, "404.html", status=404)


def handler500(request, exception=None):
    return render(request, "500.html", status=500)
