# Generated by Django 4.2 on 2024-08-03 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Менеджер команды'),
        ),
        migrations.AddField(
            model_name='product',
            name='parent_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.product', verbose_name='Родительский продукт'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Менеджер продукта'),
        ),
        migrations.AddField(
            model_name='metric',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='gazpromuserteam',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник'),
        ),
        migrations.AddField(
            model_name='gazpromuserteam',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.team', verbose_name='Команда'),
        ),
        migrations.AddField(
            model_name='department',
            name='departament_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Руководитель департамента'),
        ),
        migrations.AddField(
            model_name='department',
            name='parent_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.department', verbose_name='Родительский департамент'),
        ),
        migrations.AddField(
            model_name='component',
            name='component_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_components', to=settings.AUTH_USER_MODEL, verbose_name='Ответственный за компонент'),
        ),
        migrations.AddField(
            model_name='component',
            name='component_second_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second_owned_components', to=settings.AUTH_USER_MODEL, verbose_name='Заместитель ответственного за компонент'),
        ),
        migrations.AddField(
            model_name='additionalfield',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddIndex(
            model_name='metric',
            index=models.Index(fields=['content_type', 'object_id'], name='company_met_content_24f8ca_idx'),
        ),
        migrations.AddIndex(
            model_name='additionalfield',
            index=models.Index(fields=['content_type', 'object_id'], name='company_add_content_cdcf27_idx'),
        ),
    ]
