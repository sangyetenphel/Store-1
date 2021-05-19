from django.shortcuts import render
from .models import Product

# Create your views here.
def home(request):
    context = {
        'title': 'Home',
        'products': Product.objects.all()
    }
    return render(request, 'store/home.html', context)