from django.views import View
from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from .views import SecurityQuery

urlpatterns = [
    path('account/dashboard/', login_required(views.dashboard), name='dashboard'),
    path('account/control/', login_required(views.control), name='control'),
    path('account/profile/', login_required(views.profile), name='profile'),
    path('account/security/', login_required(SecurityQuery.as_view()), name='security'),
    path('account/settings/', login_required(views.settings), name='settings'),
    path('logout/', login_required(views.logout_request), name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)