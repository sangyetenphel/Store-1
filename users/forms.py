from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from django.forms.fields import EmailField

class UserRegistrationForm(UserCreationForm):
    # Adding email to UserCreationForm besides the default of username and password
    email = forms.EmailField()

    class Meta:
        # Save to User model after we form.save()
        model = User
        # Fields to display in order in front-end
        fields = ['username', 'email', 'password1', 'password2']