from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('account/control/', login_required(views.control), name='control'),
    path('account/create_group/', login_required(views.create_group), name='create_groups'),
]
