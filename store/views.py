from django.shortcuts import render

products = [
    {
        'name': 'Electric toothbrush',
        'price': '$30'
    },
    {
        'name': 'Bamboo toothbrush',
        'price': '$20'
    },
]

# Create your views here.
def home(request):
    context = {
        'title': 'Home',
        'products': products
    }
    return render(request, 'store/home.html', context)