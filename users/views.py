from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserRegistrationForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Will save the user to database with hashed password and all that good stuff
            form.save()
            username = form.cleaned_data.get('username')
            # One-time message send to base.html (Also: info, error, warning etc)
            messages.success(request, f'Account created for {username}!')
            return redirect('store-home')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form':form})