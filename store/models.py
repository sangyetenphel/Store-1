from django.db import models
from django.utils import timezone
from PIL import Image

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default="product_default.jpg", upload_to="product_pics")

    def  __str__(self):
        return f"{self.name} - {self.price}"

    def save(self):
        super().save()
         
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
