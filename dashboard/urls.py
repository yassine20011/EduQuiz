from django.views import View
from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from .views import SecurityQuery
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('account/', login_required(views.dashboard), name='dashboard'),
    path('account/dashboard/', login_required(views.control), name='control'),
    path('account/create_quiz/', login_required(views.create_quiz), name='create_quiz'),
    path('account/create_questions/<str:quiz_title>/', login_required(views.create_questions), name='create_questions'),
    path('account/question_form/', login_required(views.create_question_form), name='question_form'),
    path('account/quiz_preview/<str:quiz_title>/', login_required(views.view_quiz), name='quiz_preview'),
    path('account/delete_quiz/<str:quiz_title>/', login_required(views.delete_quiz), name='delete_quiz'),
    path('account/profile/', login_required(views.profile), name='profile'),
    path('account/security/', login_required(SecurityQuery.as_view()), name='security'),
    path('account/settings/', login_required(auth_views.PasswordChangeView.as_view(template_name='settings.html', success_url=reverse_lazy('password_change_done'))), name='settings'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('logout/', login_required(views.logout_request), name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)