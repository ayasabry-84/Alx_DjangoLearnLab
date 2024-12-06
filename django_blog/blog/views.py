from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm  # Assume you have a UserProfileForm for profile editing.

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import BlogPostForm


# Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after successful registration
            messages.success(request, "Registration successful!")
            return redirect('home')  # Redirect to home or any page after registration
        else:
            messages.error(request, "Error during registration. Please try again.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Login View (Using Django's built-in LoginView)
from django.contrib.auth.views import LoginView

# Logout View (Using Django's built-in LogoutView)
from django.contrib.auth.views import LogoutView

# Profile View
@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)  # Assuming a Profile model is linked to the User
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Error updating profile. Please try again.")
    else:
        profile_form = UserProfileForm(instance=request.user.profile)

    return render(request, 'registration/profile.html', {'profile_form': profile_form})

# View for user logout (optional, Django provides a built-in logout function)
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')  # Redirect to home or login page

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blog_posts'
    ordering = ['-created_at']  # Order by creation date, newest first

# Show a single blog post's details
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'blog_post'

# Create a new blog post
class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm  # Use the custom form
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:post_list')  # Redirect to the list of posts after successful creation

    def form_valid(self, form):
        form.instance.author = self.request.user  # Automatically set author to the logged-in user
        return super().form_valid(form)

# Update an existing blog post
class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm  # Use the custom form
    template_name = 'blog/blogpost_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Ensure only the author can update
        return super().form_valid(form)

    def test_func(self):
        blog_post = self.get_object()
        return blog_post.author == self.request.user  # Ensure only the author can edit

# Delete a blog post
class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')  # Redirect after successful deletion

    def test_func(self):
        blog_post = self.get_object()
        return blog_post.author == self.request.user  # Ensure only the author can delete