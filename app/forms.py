from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Post, Rubric
from django.forms import ModelForm
from django import forms

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class CreateAndUpdatePostForm(ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'name' : 'title',
            'placeholder' : '...',
            'required' : True,
        })
    )

    class Meta:
        model = Post
        fields = ('title','content','price','contact','image','rubric')