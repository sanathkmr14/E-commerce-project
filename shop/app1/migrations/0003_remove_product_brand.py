# Generated by Django 4.2.2 on 2023-06-11 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_rename_product_cart_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
    ]
