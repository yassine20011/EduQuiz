from dashboard.models import ClassRoom, Profile, Quiz, Question, Answer
from .forms import CreateGroupForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

def control(request):
    return render(request, 'control.html', {})

@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def create_group(request):
    groups = ClassRoom.objects.all()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.name = form.cleaned_data['name']
            group.created_by = request.user
            group.save()
            return redirect('control')
        else:
            messages.error(request, 'Something went wrong!')
            redirect('control')
        
        
    form = CreateGroupForm()
    return render(request, 'create_group.html', {'create_group_form': form, 'groups': groups})