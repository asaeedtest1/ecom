from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile

# Placeholder for accounts views

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        errors = []
        if not email:
            errors.append('Email is required.')
        if not phone:
            errors.append('Phone is required.')
        if not address:
            errors.append('Address is required.')
        if errors:
            return render(request, 'profile_edit.html', {'profile': profile, 'errors': errors, 'email': email, 'phone': phone, 'address': address})
        # Update user email and profile fields
        request.user.email = email
        request.user.save()
        profile.phone = phone
        profile.address = address
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'profile_edit.html', {
        'profile': profile,
        'email': request.user.email,
        'phone': profile.phone,
        'address': profile.address,
    })
