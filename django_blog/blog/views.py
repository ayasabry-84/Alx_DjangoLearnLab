from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm  # Assume you have a UserProfileForm for profile editing.

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
