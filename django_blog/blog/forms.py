from django import forms
from .models import Post

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile  # Import the UserProfile model

from .models import Comment

from taggit.forms import TagWidget  # Import TagWidget for tag management
from .models import Tag  # Import the Tag model if it's in the same app
from taggit.forms import TagField



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Default user fields

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(required=False)
    
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']

    # Override to save both user and profile data
    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user_profile.user.email = self.cleaned_data['email']
        if commit:
            user_profile.user.save()  # Save user email
            user_profile.save()  # Save profile data
        return user_profile


class PostForm(forms.ModelForm):
    tags = TagField(required=False)
    
    class Meta:
        model = Post
        fields = ['title', 'content' , 'author' , 'tags']
    
    

    def clean_tags(self):
        """
        Convert the entered tags into tag objects if they don't exist.
        """
        tags = self.cleaned_data['tags']
        tag_names = [tag.strip() for tag in tags.split(',')]
        return tag_names
    
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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Include fields you want the user to fill
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4,
            }),
        }
        labels = {
            'content': 'Your Comment',
        }

def clean_content(self):
    content = self.cleaned_data.get('content')
    if len(content) < 5:
        raise forms.ValidationError("Comment must be at least 5 characters long.")
    return content
