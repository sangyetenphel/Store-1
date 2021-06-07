from django.db import models
from django.db.models.base import Model, ModelState
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    keyword = models.CharField(max_length=255)
    date_added = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='products')
    description = RichTextUploadingField()
    # amount = models.IntegerField()
    # min_amount = models.IntegerField()
    # status = models.BooleanField()

    def  __str__(self):
        return self.name

    def save(self):
        super().save()
         
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def image_tag(self):
        # mark_safe as an html for output in the admin page
        return mark_safe(f'<img src="{self.image.url}" height="50">')

    image_tag.short_description = "Product Image"


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to="products")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Images"


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150, blank=True)
    review = models.TextField(blank=True)
    rating = models.IntegerField()
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review

    def get_absolute_url(self):
        return reverse('review-product', kwargs={'pk': self.product.id})


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.name

    @property
    def price(self):
        return self.product.price

    @property
    def amount(self):
        return self.quantity * self.product.price
