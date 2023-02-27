from dashboard.models import ClassRoom, Profile, Quiz, Question, Answer
from django.forms import ModelForm
from django import forms



class CreateGroupForm(ModelForm):
    name = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = ClassRoom
        fields = ['name']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = False
        self.fields['name'].widget.attrs.update({'class': 'form-control'})

