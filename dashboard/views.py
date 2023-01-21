from statistics import mode
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UpdateUserForm, UpdateAvatarBio
from .models import DataRelatedToUser, Profile
from django.contrib.auth import logout
from django.views.generic.list import ListView 


def dashboard(request):
    return render(request, 'dashboard.html',)


#Profile view 
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateAvatarBio(request.POST, request.FILES, instance=request.user.profile)

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

def settings(request):
    return render(request, 'settings.html')



from django.contrib.auth.forms import PasswordResetForm




class SecurityQuery(ListView):
    model = DataRelatedToUser
    context_object_name = "ip_adresse"
    template_name = 'security.html'
    def get_queryset(self):  # sourcery skip: inline-immediately-returned-variable
        profile = Profile.objects.get(user=self.request.user)
        ip_addresses = DataRelatedToUser.objects.filter(profile=profile).order_by('-date')
        return ip_addresses
        
    def get_context_data(self, **kwargs):
        context = super(SecurityQuery, self).get_context_data(**kwargs)
        context['change_password'] = PasswordResetForm(self.request.POST)
        return context

def logout_request(request):
    logout(request)
    return redirect("home")