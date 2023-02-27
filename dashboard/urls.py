from django.views import View
from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from .views import SecurityQuery
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import TemplateView


handler404 = 'dashboard.views.handler404'
handler500 = 'dashboard.views.handler500'


# A list of all the urls that the app will use.
urlpatterns = [
    path('account/', login_required(views.dashboard), name='dashboard'),
    path('account/dashboard/', login_required(views.dashboard1), name='dashboard1'),
    path('account/create_quiz/', login_required(views.create_quiz), name='create_quiz'),
    path('account/quiz_preview/<str:quiz_title>/', login_required(views.view_quiz), name='quiz_preview'),
    path('account/results_with_details/<str:quiz_title>/', login_required(views.results_with_details), name='results_with_details'),
    path('account/standard_results/<str:quiz_title>/', login_required(views.standard_results), name='standard_results'),
    path('account/delete_quiz/<str:quiz_title>/', login_required(views.delete_quiz), name='delete_quiz'),
    path('account/available_quizzes/', login_required(views.available_quizzes), name='available_quizzes'),
    path('account/take_quiz/<str:quiz_title>/', login_required(views.take_quiz), name='take_quiz'),
    path('account/groups/', login_required(views.join_groups), name='groups'),
    path('account/join_group/<str:group_name>/', login_required(views.join_groups), name='join_group'),
    path('account/profile/', login_required(views.profile), name='profile'),
    path('account/security/', login_required(SecurityQuery.as_view()), name='security'),
    path('account/settings/', login_required(auth_views.PasswordChangeView.as_view(template_name='settings.html', success_url=reverse_lazy('password_change_done'))), name='settings'),
    path('thank_you/', login_required(TemplateView.as_view(template_name="thanks.html")), name='thank_you'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('logout/', login_required(views.logout_request), name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


