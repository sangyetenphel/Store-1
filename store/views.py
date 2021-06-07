from django.contrib import messages
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import DeleteView
from .models import Product, Review, Cart
from .forms import ReviewForm, CartForm

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


def product(request, id):
    product = Product.objects.get(pk=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = Review()
            new_review.subject = form.cleaned_data['subject']
            new_review.review = form.cleaned_data['review']
            new_review.rating = form.cleaned_data['rating']
            new_review.product = product
            new_review.reviewer = request.user
            new_review.save()
            messages.success(request, "Thank you for reviewing our product.")
            # Return back to the prev page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))            
    context = {
        'product': product,
        'reviews': Review.objects.filter(product=product).order_by('-date_added')[:2]
        }
    return render(request, 'store/product.html', context)

@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user)
    sub_total = 0
    tax = 20
    for order in cart:
        sub_total += order.amount

    context = {
        'cart': cart,
        'sub_total': sub_total,
        'total': sub_total + tax
    }
    return render(request, 'store/cart.html', context)


def add_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if Cart.objects.filter(product_id=id):
                cart = Cart.objects.get(product_id=id)
                cart.quantity += quantity
            else:
                cart = Cart()
                cart.user = request.user
                cart.product = product
                cart.quantity = quantity
            cart.save()
            messages.success(request, "Your product has been added to cart!")
        else:
            print(form.errors)
            return HttpResponse(form.errors)
            
    return HttpResponseRedirect(url)


def delete_cart(request, id):
    Cart.objects.filter(id=id).delete()
    messages.success(request, "The item has been removed from your cart.")
    return redirect('cart')