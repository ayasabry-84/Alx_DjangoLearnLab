# blog/forms.py

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

    # Automatically set the author to the current logged-in user
    def save(self, user, commit=True):
        blog_post = super().save(commit=False)
        blog_post.author = user  # Set the author to the provided user
        if commit:
            blog_post.save()
        return blog_post

    # Make sure the 'content' field isn't empty
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("Content cannot be empty.")
        return content
