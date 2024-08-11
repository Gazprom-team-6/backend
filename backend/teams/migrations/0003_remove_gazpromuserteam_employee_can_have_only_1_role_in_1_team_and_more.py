# Generated by Django 4.2 on 2024-08-11 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='gazpromuserteam',
            name='Employee can have only 1 role in 1 team',
        ),
        migrations.AddConstraint(
            model_name='gazpromuserteam',
            constraint=models.UniqueConstraint(fields=('employee', 'team'), name='one_employee_role_in_one_team'),
        ),
    ]
