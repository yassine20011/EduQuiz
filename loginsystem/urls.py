from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    #path('account/profile', login_required(TemplateView.as_view(template_name='pages/dashboard.html')), name='dashboard'),
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('accounts/login/', views.login, name='login'),
    #path('change/password/', views.Password().change_password, name='change_password'),
    #path('change/new_password/', views.Password().new_password, name='new_password'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),

]