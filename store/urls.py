from django.conf.urls import url
from django.urls import path
from django.urls import path
from . import views
from .views import ReviewDetailView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    path('', views.home, name='store-home'),
    path('review/<int:pk>', ReviewDetailView.as_view(), name='review-product'),
    path('review/<int:product_id>/new', ReviewCreateView.as_view(), name='review-new'),
    path('review/<int:pk>/update', ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/delete', ReviewDeleteView.as_view(), name='review-delete'),

    path('products', views.products, name='products'),
    path('cart', views.cart, name='cart'),
]