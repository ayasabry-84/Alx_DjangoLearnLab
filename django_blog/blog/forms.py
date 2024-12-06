# blog/forms.py

from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']

    # Automatically set the author to the current logged-in user
    def save(self, commit=True):
        blog_post = super().save(commit=False)
        if commit:
            blog_post.author = self.user
            blog_post.save()
        return blog_post

    # Make sure the 'content' field isn't empty
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("Content cannot be empty.")
        return content
