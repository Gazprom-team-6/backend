# Generated by Django 4.2 on 2024-08-07 09:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=250, unique=True, verbose_name='Название')),
                ('product_description', models.TextField(verbose_name='Описание продукта')),
                ('parent_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_product', to='products.product', verbose_name='Родительский продукт')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'Продукты',
                'default_related_name': 'product',
            },
        ),
    ]
