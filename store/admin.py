from django.contrib import admin
from .models import Product, Review, Images, Cart

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline]


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'price', 'amount']


admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
admin.site.register(Images)
admin.site.register(Cart, CartAdmin)

