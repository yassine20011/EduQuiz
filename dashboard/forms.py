from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import DataRelatedToUser


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
  
class UpdateAvatarBio(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'block w-full mb-5 text-xs text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'}))
    bio = forms.CharField(max_length=150, required=False)
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

