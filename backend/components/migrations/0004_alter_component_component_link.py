# Generated by Django 4.2 on 2024-08-07 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0003_remove_component_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='component_link',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на документацию'),
        ),
    ]
