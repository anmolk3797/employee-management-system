# Generated by Django 5.0.1 on 2024-01-05 12:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("employee", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "department_type",
                    models.CharField(
                        choices=[
                            ("recruitment", "Recruitment"),
                            ("IT", "IT"),
                            ("finance", "Finance"),
                            ("management", "Management"),
                            ("other", "Other"),
                        ],
                        max_length=32,
                    ),
                ),
                ("status", models.IntegerField()),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employee_departments",
                        to="employee.employees",
                    ),
                ),
            ],
        ),
    ]