from django.contrib import admin
from django.contrib.auth import models
from .models import Product, Review, Images, Cart, OrderProduct, Order, Variant

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 3


class ProductVariantInline(admin.TabularInline):
    model = Variant
    extra = 1
    show_change_link = True


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline, ProductVariantInline]


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'price', 'amount']


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'price', 'quantity', 'amount')
    can_delete = False
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'street_address', 'apt_number', 'city', 'state', 'zip_code', 'country' ]
    inlines = [OrderProductInline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price', 'quantity', 'amount']
    list_filter = ['user']


admin.site.register(Product, ProductAdmin)
admin.site.register(Variant)
admin.site.register(Review)
admin.site.register(Images)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)


