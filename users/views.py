from store.models import Review
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store-home')
        else:
            messages.warning(request, "Login Error! Username or password is incorrect.")
    return render(request, 'users/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'See you soon!')
    return redirect('store-home')


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Will save the user to database with hashed password and all that good stuff
            form.save()
            username = form.cleaned_data.get('username')
            # One-time message send to base.html (Also: info, error, warning etc)
            messages.success(request, f'Account created for {username}!')
            return redirect('user-login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form':form})


@login_required
def user_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) 
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    reviews = Review.objects.filter(reviewer=request.user)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'reviews': reviews,
    }
    return render(request, 'users/profile.html', context)


def user_review_delete(request, id):
    Review.objects.get(pk=id).delete()
    messages.success(request, 'Your review has been deleted.')
    return redirect('user-profile')
