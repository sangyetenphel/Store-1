# Generated by Django 3.2.3 on 2021-05-21 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='product_default.jpg', upload_to='product_pics'),
        ),
    ]