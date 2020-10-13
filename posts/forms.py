from django import forms
from .models import Post

MAX_TITLE_LENGTH = 128
MAX_SUMMARY_LENGTH = 256

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'summary', 'content']

    def clean(self):
        data = {
            'title': self.cleaned_data.get('title'),
            'summary': self.cleaned_data.get('summary'),
            'content': self.cleaned_data.get('content')
        }
        if len(data['title']) > MAX_TITLE_LENGTH:
            raise forms.ValidationError(f"The title must not be more than {MAX_TITLE_LENGTH} characters long.")
        if len(data['summary']) > MAX_SUMMARY_LENGTH:
            raise forms.ValidationError(f"The summary must not be more than {MAX_SUMMARY_LENGTH} characters long.")
        return data