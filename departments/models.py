from django.db import models
from employee.models import Employees



class Department(models.Model):
    Department_CHOICES = [
        ('recruitment', 'Recruitment'),
        ('IT', 'IT'),
        ('finance', 'Finance'),
        ('management','Management'),
        ("other","Other"),
    ]
    employee = models.ForeignKey(
        Employees, related_name="employee_departments", on_delete=models.CASCADE
    )
    department_type = models.CharField(
        max_length=32, choices=Department_CHOICES)
    status = models.IntegerField() 

    def __str__(self):
        return f"{self.employee}/{self.department_type}"

