from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from post.models import Comment, Post
from ckeditor.widgets import CKEditorWidget


class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model=User
        fields=['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        

class PostForm(forms.ModelForm):
    post = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = ['title', 'post_category', 'post_image', 'post']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']