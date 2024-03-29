from django.shortcuts import render
from .models import Department
from  departments.serializers import DepartmentSerializer
from django.db import connection
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required   
from django.http import HttpResponse
import json
from django.shortcuts import get_object_or_404

from employee.models import Employees
from django.http import JsonResponse


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
    def create(self, request):
        data = request.data
        resp = {'status': 'failed'}
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO departments_department (department_type, employee_id, status)
                    VALUES (%s, %s, %s)
                """, [data['department_type'], data['employee'], data['status']])
                resp['status'] = 'success'

        except Exception as e:
            resp['error'] = str(e)

        return Response(resp, status=status.HTTP_201_CREATED if resp['status'] == 'success' else status.HTTP_400_BAD_REQUEST)



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
    try:
        # Fetch the department - your logic to determine which department to fetch
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT department.id, department.department_type,
                       employee.id AS employee_id, employee.firstname, employee.lastname
                FROM departments_department AS department
                JOIN employee_employees AS employee ON department.employee_id = employee.id
                LIMIT 1  /* Fetching the first department, modify this as needed */
            """)
            row = cursor.fetchone()

        if row:
            department = {
                'id': row[0],
                'department_type': row[1],
                'employee_id': row[2],
                'employee_firstname': row[3],
                'employee_lastname': row[4],
            }

            # Fetch all employees
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, firstname, lastname
                    FROM employee_employees
                """)
                employee_rows = cursor.fetchall()

            employees = [{
                'id': emp[0],
                'firstname': emp[1],
                'lastname': emp[2],
            } for emp in employee_rows]

            context = {
                'department': department,
                'employees': employees,
            }
            return render(request, 'employee/manage_departments.html', context)
        else:
            return HttpResponse("Department not found")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

@login_required
def save_department(request):
    if request.method == 'POST':
        data = request.POST
        resp = {'status': 'failed'}
        try:
            employee_id = data.get('employee')
            if employee_id:
                employee_exists = Employees.objects.filter(id=employee_id).first()
                if employee_exists:
                    department = Department(
                        department_type=data['department_type'],
                        employee=employee_exists,
                        status=data['status']
                    )
                    department.save()
                    resp['status'] = 'success'
                else:
                    resp['error'] = 'Employee does not exist'
            else:
                resp['error'] = 'Invalid employee ID'
        except Exception as e:
            resp['error'] = str(e)

        return JsonResponse(resp)
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
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

