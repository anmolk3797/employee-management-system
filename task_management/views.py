from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from employee.models import Employees  # Import the Employees model
from task_management.serializers import TaskSerializer
from task_management.models import Task
from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  
from django.http import HttpResponse
import json
from rest_framework import viewsets,status
from django.http import JsonResponse


class TaskModelViewset(viewsets.ViewSet):
    serializer_class = TaskSerializer

    def list(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT task.id, task.title, task.description, task.task_status, task.estimated_time,
                       employee.id AS employee_id, employee.firstname, employee.lastname
                FROM task_management_task AS task
                JOIN employee_employees AS employee ON task.employee_id_id = employee.id
            """)
            results = cursor.fetchall()

        tasks_data = [
            {
                'id': result[0],
                'title': result[1],
                'description': result[2],
                'task_status': result[3],
                'estimated_time': result[4],
                'employee_id': result[5],
                'employee_firstname': result[6],
                'employee_lastname': result[7],
            }
            for result in results
        ]

        return Response(tasks_data)
    
    def create(self, request):
        data = request.data
        resp = {'status': 'failed'}
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO task_management_task (title, description, task_status, estimated_time, employee_id_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, [data['title'], data['description'], data['task_status'], data['estimated_time'], data['employee_id']])
                resp['status'] = 'success'
        except Exception as e:
            resp['error'] = str(e)

        return Response(resp, status=status.HTTP_201_CREATED if resp['status'] == 'success' else status.HTTP_400_BAD_REQUEST)

 #Positions
@login_required
def task_list(request):
    task_list = Task.objects.all()
    context = {
        'page_title':'Task Management',
        'positions':task_list,
    }
    return render(request, 'employee/tasks.html',context)
@login_required
def manage_tasks(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    task.id, task.title, task.description, 
                    task.task_status, task.estimated_time,
                    employee.id AS employee_id,
                    employee.firstname AS employee_firstname,
                    employee.lastname AS employee_lastname
                FROM task_management_task AS task
                INNER JOIN employee_employees AS employee 
                    ON task.employee_id_id = employee.id
            """)
            rows = cursor.fetchall()

        tasks_data = []
        for row in rows:
            task_data = {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'task_status': row[3],
                'estimated_time': row[4],
                'employee_id': row[5],
                'employee_firstname': row[6],
                'employee_lastname': row[7],
            }
            tasks_data.append(task_data)
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
            'tasks': tasks_data,
            'employees': employees
        }
        return render(request, 'employee/manage_tasks.html', context)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

@login_required
def save_tasks(request):
    if request.method == 'POST':
        data = request.POST
        resp = {'status': 'failed'}
        try:
            employee_id = data.get('employee')
            if employee_id:
                employee_exists = Employees.objects.filter(id=employee_id).first()
                if employee_exists:
                    task = Task(
                        title=data['title'],
                        description=data['description'],
                        task_status=data['task_status'],
                        estimated_time=data['estimated_time'],
                        employee_id=employee_exists
                    )
                    task.save()
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
def delete_tasks(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Task.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")