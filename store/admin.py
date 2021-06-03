from django.contrib import admin
from .models import Product, Review, Images

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 3

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_tag']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
admin.site.register(Images)

