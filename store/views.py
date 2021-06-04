from django.http import request
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls.base import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import DeleteView
from .models import Product, Review

# Create your views here.
def home(request):
    context = {
        'title': 'Home',
        'products': Product.objects.all(),
        'latest_products': Product.objects.order_by('-date_added')[:4]
    }
    return render(request, 'store/home.html', context)


class ReviewDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the reviews of a particular Product
        context['reviews'] = Review.objects.filter(product=self.kwargs.get('pk'))
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['review'] 

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        form.instance.product = Product.objects.get(pk=self.kwargs['product_id'])
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['review'] 

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """So User can only edit his/her own review"""
        review = self.get_object()
        if self.request.user == review.reviewer:
            return True
        else:
            return False 


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review

    def get_success_url(self):
        product = self.object.product
        return reverse_lazy('review-product', kwargs={'pk': product.id})

    def test_func(self):
        """So User can only edit his/her own review"""
        review = self.get_object()
        if self.request.user == review.reviewer:
            return True
        else:
            return False 

def products(request):
    context = {
        'products': Product.objects.all()
    }
    
    return render(request, 'store/products.html', context)

def cart(request):
    return render(request, 'store/cart.html')