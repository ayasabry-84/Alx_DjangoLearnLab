from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm  # Assume you have a UserProfileForm for profile editing.

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from .forms import CustomUserCreationForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.views import LoginView, LogoutView

from .forms import PostForm



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
#________________________________________________________________________________________
#________________________________________________________________________________________
#________________________________________________________________________________________



class BlogPostListView(ListView):
    model = Post
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blog_posts'
    ordering = ['-created_at']  # Order by creation date, newest first

# Show a single blog post's details
class BlogPostDetailView(DetailView):
    model = Post
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'blog_post'

# Create a new blog post
class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm  # Use the custom form
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:post_list')  # Redirect to the list of posts after successful creation

    def form_valid(self, form):
        form.instance.author = self.request.user  # Automatically set author to the logged-in user
        return super().form_valid(form)

# Update an existing blog post
class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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
class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')  # Redirect after successful deletion

    def test_func(self):
        blog_post = self.get_object()
        return blog_post.author == self.request.user  # Ensure only the author can delete