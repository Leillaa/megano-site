# Generated by Django 4.1.7 on 2023-03-25 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='product',
        ),
        migrations.AddField(
            model_name='tag',
            name='product',
            field=models.ManyToManyField(related_name='tags', to='products.product', verbose_name='тэг'),
        ),
    ]