import json 
import stripe

from django.contrib import messages
# from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt 
from django.shortcuts import redirect, render

# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
# from django.urls.base import reverse_lazy
from django.template.loader import render_to_string
from django.views.generic import TemplateView
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.views.generic.edit import DeleteView
from .models import Color, Order, Product, ProductVariant, Review, Cart, OrderProduct, Color, Size
from .forms import ReviewForm, CartForm, OrderForm

# Create your views here.
def home(request):
    context = {
        'title': 'Home',
        'products': Product.objects.all(),
        'latest_products': Product.objects.order_by('-date_added')[:4]
    }
    return render(request, 'store/home.html', context)


# class ReviewDetailView(DetailView):
#     model = Product

#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in a QuerySet of all the reviews of a particular Product
#         context['reviews'] = Review.objects.filter(product=self.kwargs.get('pk'))
#         return context


# class ReviewCreateView(LoginRequiredMixin, CreateView):
#     model = Review
#     fields = ['review'] 

#     def form_valid(self, form):
#         form.instance.reviewer = self.request.user
#         form.instance.product = Product.objects.get(pk=self.kwargs['product_id'])
#         return super().form_valid(form)


# class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Review
#     fields = ['review'] 

#     def form_valid(self, form):
#         form.instance.reviewer = self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         """So User can only edit his/her own review"""
#         review = self.get_object()
#         if self.request.user == review.reviewer:
#             return True
#         else:
#             return False 


# class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Review

#     def get_success_url(self):
#         product = self.object.product
#         return reverse_lazy('review-product', kwargs={'pk': product.id})

#     def test_func(self):
#         """So User can only edit his/her own review"""
#         review = self.get_object()
#         if self.request.user == review.reviewer:
#             return True
#         else:
#             return False 

            

def products(request):
    context = {
        'products': Product.objects.all()
    }
    
    return render(request, 'store/products.html', context)


def product(request, id):
    product = Product.objects.get(pk=id)
    context = {
        'product': product,
        'reviews': Review.objects.filter(product=product).order_by('-date_added')[:2],
    }

    if request.method == 'POST':
       pass
    else:
        variants = ProductVariant.objects.filter(product_id=id)
        if variants:
            sizes = ProductVariant.objects.raw('SELECT * FROM store_productvariant WHERE product_id=%s GROUP BY size_id',[id])
            colors = ProductVariant.objects.filter(product=product, size=variants[0].size)
            variant = ProductVariant.objects.get(id=variants[0].id) 
            context.update({
                'sizes': sizes,
                'colors': colors,
                'variant': variant
            })   

    return render(request, 'store/product.html', context)


def ajax_sizes(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        product_id = body['productId']
        size_id = body['size']
        colors = ProductVariant.objects.filter(product_id=product_id, size_id=size_id)
        context = {
            'size_id': size_id,
            'product_id': product_id,
            'colors': colors
        }
        data = {'rendered_table': render_to_string('store/product_color_variants.html', context=context)}
        return JsonResponse(data)


def review_product(request):
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
        print(request.POST)
        if request.POST['variant']:
            color_id = request.POST['color']
            size_id = request.POST['size']
            variant = ProductVariant.objects.filter(product_id=id, size_id=size_id, color_id=color_id)[0]
        else: 
            variant = None
        form = CartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            # Check if the Product with the specific variant is already in Cart or not
            if Cart.objects.filter(product_id=id, variant=variant):
                cart = Cart.objects.get(product_id=id)
                cart.quantity += quantity
            else:
                cart = Cart()
                cart.user = request.user
                cart.product = product
                cart.variant = variant
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


# def order(request):
#     cart = Cart.objects.filter(user=request.user)
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             # Send credit card info to bank, If the bank responds ok, continue, if not, show the error

#             order = form.save(commit=False)
#             order.user = request.user
#             order.save()

#             for cart_item in cart:
#                 order_product = OrderProduct()
#                 order_product.order_id = order.id
#                 order_product.product = cart_item.product
#                 order_product.user = request.user
#                 order_product.quantity = cart_item.quantity
#                 order_product.price = cart_item.product.price
#                 order_product.amount = order_product.quantity * order_product.price
#                 order_product.save()
#             # cart.delete()
#             # messages.success(request, 'Your order has been completed!')
#             return render(request, 'store/checkout.html')
#     else:
#         form = OrderForm()
#         context = {
#             'form': form,
#         }
#         return render(request, 'store/order.html', context)


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        prev_url = request.META.get('HTTP_REFERER')
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            cart = Cart.objects.filter(user=request.user)
            line_items = []
            for item in cart:
                if item.variant:
                    name =  item.variant.title
                    images = [domain_url + item.variant.image()] 
                else:
                    name = item.product.name
                    images = [domain_url + item.product.image.url]
                line_items_dic = {'price_data': {}}
                line_items_dic['price_data'] = {
                    'currency': 'usd',
                    'unit_amount': int(item.price * 100),
                    'product_data': {
                        'name': name,
                        'images': images,
                    }
                }
                line_items_dic['quantity'] = item.quantity
                
                line_items.append(line_items_dic)
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                # billing_address_collection = 'required',
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                payment_method_types=['card'],  
                
                # shipping_rates=['shr_123456789'],
                shipping_address_collection={
                    'allowed_countries': ['US', 'CA'],
                },
                # line_items=[
                #     {
                #         'price_data': {
                #             'currency': 'usd',
                #             'unit_amount': 2000,
                #             'product_data': {
                #                 'name': 'Stubborn Attachments',
                #                 'images': ['https://i.imgur.com/EHyR2nP.png'],
                #             },
                #         },
                #         'quantity': 1,
                #     },
                # ],
                line_items = line_items,
                metadata = {
                    # 'product_id': product.id,
                    'user_id': request.user.id
                },
                mode='payment',
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url= prev_url,
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        session = event['data']['object']
        print(session)
        print(request.user)
        user_id = session['metadata']['user_id']
        Cart.objects.filter(user_id=user_id).delete()
        
        # amount_shipping = session.total_details.amount_shipping
        # TODO: run some custom code here

    return HttpResponse(status=200)


class SuccessView(TemplateView):
    template_name = 'store/success.html'


# class CancelledView(TemplateView):
#     template_name = 'store/cancelled.html'