# Generated by Django 4.1.7 on 2023-03-23 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_reviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salePrice', models.DecimalField(db_index=True, decimal_places=2, default=0, max_digits=10, verbose_name='цена')),
                ('dateFrom', models.DateField(default='', verbose_name='старт продаж')),
                ('dateTo', models.DateField(default='', verbose_name='окончание продаж')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='products.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'распродажа',
                'verbose_name_plural': 'распродажи',
            },
        ),
    ]
