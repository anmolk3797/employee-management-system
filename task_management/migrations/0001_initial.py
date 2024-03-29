# Generated by Django 5.0.1 on 2024-01-05 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('description', models.TextField()),
                ('task_status', models.CharField(choices=[('pending', 'Pending'), ('work in progress', 'Work In Progress'), ('done', 'Done'), ('other', 'Other')], max_length=60)),
                ('estimated_time', models.FloatField(default=0, help_text='Estimated time for complete the task(Estimated Time of Arrival)')),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_tasks', to='employee.employees')),
            ],
        ),
    ]
