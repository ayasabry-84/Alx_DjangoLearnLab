from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm  # Assume you have a UserProfileForm for profile editing.

from django.views import View
from .forms import CustomUserCreationForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.views import LoginView, LogoutView

from .forms import PostForm

from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

from .models import Tag  # Import the Tag model if it's in the same app


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            messages.success(request, "Registration successful!")
            return redirect('home')  # Redirect to home page or any other page after successful registration
        else:
            messages.error(request, "Error during registration. Please try again.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    # Get the user's current profile
    user_profile = request.user.profile
    
    if request.method == 'POST':
        # If the form is submitted, bind the form with the POST data and the current profile data
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()  # Save the form data
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  # Redirect to the profile page to show updated info
        else:
            messages.error(request, "Error updating profile. Please try again.")
    else:
        # Display the form with the current profile data
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'registration/profile.html', {'profile_form': profile_form})


def user_logout(request):
    logout(request)  # Log the user out
    return redirect('login')  # Redirect to login page or home page


class PostListView(ListView):
    model = Post
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blog_posts'
    ordering = ['-created_at']  # Order by creation date, newest first

# Show a single blog post's details
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'blog_post'

# Create a new blog post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm  # Use the custom form
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:post_list')  # Redirect to the list of posts after successful creation

    def form_valid(self, form):
        form.instance.author = self.request.user  # Automatically set author to the logged-in user
        return super().form_valid(form)

# Update an existing blog post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm  # Use the custom form
    template_name = 'blog/blogpost_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Ensure only the author can update
        return super().form_valid(form)

    def test_func(self):
        blog_post = self.get_object()
        return blog_post.author == self.request.user  # Ensure only the author can edit

# Delete a blog post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')  # Redirect after successful deletion

    def test_func(self):
        blog_post = self.get_object()
        return blog_post.author == self.request.user  # Ensure only the author can delete
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'object': post,
        'comments': comments,
        'form': form
    })

class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_by_tag.html'  # The template that will display the posts
    context_object_name = 'posts'  # Name of the context variable in the template

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']  # Get the tag name from the URL
        tag = get_object_or_404(Tag, name=tag_name)  # Retrieve the tag object
        return Post.objects.filter(tags=tag)  # Filter posts by the tag
    
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/edit_comment.html'

    # Ensure that only the logged-in user can edit their own comment
    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def form_valid(self, form):
        # Optionally, you can add custom behavior here if needed
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the post detail page after successfully editing the comment
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})
    
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/confirm_delete_comment.html'

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this comment.")
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_comment.html', {'form': form, 'comment': comment})

# Delete a comment
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")
    
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail', pk=post_pk)

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Save the post instance
            post = form.save()
            # The tags will be automatically saved by django-taggit
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

def search_posts(request):
    query = request.GET.get('q', '')  # Get the search query from the URL parameters

    if query:
        # Search posts by title, content, or tag name
        posts = Post.objects.filter(
            title__icontains=query  # Case-insensitive search in the title
        ).filter(
            content__icontains=query  # Case-insensitive search in the content
        ).filter(
            tags__name__icontains=query  # Case-insensitive search in tag names
        ).distinct()  # Ensure posts are only shown once

    else:
        posts = Post.objects.all()  # If no query, show all posts

    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})