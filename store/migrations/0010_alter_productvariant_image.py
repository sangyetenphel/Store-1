# Generated by Django 3.2.3 on 2021-06-15 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20210614_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.productimage'),
        ),
    ]
