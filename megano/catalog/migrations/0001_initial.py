# Generated by Django 4.1.7 on 2023-03-23 08:36

import catalog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=128, verbose_name='название')),
                ('active', models.BooleanField(default=False, verbose_name='активная')),
                ('favourite', models.BooleanField(default=False, verbose_name='избранная категория')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subcategories', to='catalog.category', verbose_name='родитель')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'ordering': ['title', 'pk'],
            },
        ),
        migrations.CreateModel(
            name='CategoryIcons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.FileField(max_length=500, upload_to=catalog.models.category_image_directory_path, verbose_name='иконка')),
                ('category', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image', to='catalog.category', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'иконка категории',
                'verbose_name_plural': 'иконки категорий',
                'ordering': ['pk'],
            },
        ),
    ]
