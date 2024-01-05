from django.db import models
from datetime import datetime
from django.db import models
from django.utils import timezone
# from phonenumber_field.modelfields import PhoneNumberField
from employee.validators import validate_pdf_extension

# Create your models here.

class Employees(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    code = models.CharField(max_length=100,blank=True) 
    firstname = models.CharField(max_length=50) 
    middlename = models.TextField(max_length=50,blank=True,null= True) 
    lastname = models.CharField(max_length=50) 
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    dob = models.DateField(blank=True,null= True) 
    contact = models.IntegerField(blank=True, null=True)
    address = models.TextField() 
    email = models.TextField() 
    date_hired = models.DateField() 
    document = models.FileField(upload_to='employee_documents/', validators=[validate_pdf_extension])
    manager_name = models.CharField(max_length=100)
    salary = models.FloatField(default=0) 
    status = models.IntegerField() 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.firstname + ' ' +self.middlename + ' '+self.lastname + ' '
    
    class Meta:
        verbose_name_plural = "Employee"

