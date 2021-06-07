from django.contrib.auth import models
from django.forms import ModelForm, fields
from .models import Review, Cart

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['subject', 'review', 'rating']


class CartForm(ModelForm):
    class Meta:
        model = Cart    
        fields = ['quantity']