from django.forms import ModelForm
from .models import Comment
from django import forms


class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['name', 'email', 'body']


class EmailPostForm(forms.Form):
	name = forms.CharField(max_length=100)
	email = forms.EmailField()
	to = forms.EmailField()
	comment = forms.CharField(widget=forms.Textarea, required=False)


