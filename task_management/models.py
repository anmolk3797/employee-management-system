from django.db import models

from employee.models import  Employees

class Task(models.Model):
    TASK_CHOICES = [
        ('pending', 'Pending'),
        ('work in progress', 'Work In Progress'),
        ('done', 'Done'),
        ("other","Other"),
    ]
    employee_id = models.ForeignKey(Employees,related_name="employee_tasks",on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=True)
    description = models.TextField()
    task_status = models.CharField(max_length=60, choices=TASK_CHOICES)
    estimated_time = models.FloatField( default=0, help_text="Estimated time for complete the task(Estimated Time of Arrival)")

