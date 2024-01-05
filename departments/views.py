from django.shortcuts import render
from .models import Department
from  departments.serializers import DepartmentSerializer
from django.db import connection
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required   
from django.http import HttpResponse
import json

class DepartmentModelViewset(viewsets.ViewSet):
    serializer_class = DepartmentSerializer  # Replace with your actual serializer

    def list(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT department.id, department.department_type,
                       employee.id AS employee_id, employee.firstname, employee.lastname
                FROM departments_department AS department
                JOIN employee_employees AS employee ON department.employee_id = employee.id
            """)
            results = cursor.fetchall()

        departments_data = [
            {
                'id': result[0],
                'department_type': result[1],
                'employee_id': result[2],
                'employee_firstname': result[3],
                'employee_lastname': result[4],
            }
            for result in results
        ]
        return Response(departments_data)



# Departments
@login_required
def departments(request):

    # Fetch the queryset using get_queryset
    department_list = Department.objects.all()
    context = {
        'page_title':'Departments',
        'departments':department_list,
    }
    return render(request, 'employee/departments.html',context)
@login_required
def manage_departments(request):
    department = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            department = Department.objects.filter(id=id).first()
    
    context = {
        'department' : department
    }
    return render(request, 'employee/manage_departments.html',context)

@login_required
def save_department(request):
    data =  request.POST
    resp = {'status':'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_department = Department.objects.filter(id = data['id']).update(department_type=data['name'], employee = data['employee'],status = data['status'])
        else:
            save_department = Department(department_type=data['name'], description = data['description'],status = data['status'])
            save_department.save()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_department(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Department.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

