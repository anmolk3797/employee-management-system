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
    task = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            task = Task.objects.filter(id=id).first()
        employee_id = Employees.objects.filter(id =id ).first()
    
    context = {
        'position' : task,
        "employee" : employee_id
    }
    return render(request, 'employee/manage_tasks.html',context)

@login_required
def save_tasks(request):
    if request.method == 'POST':
        # Get the data from the POST request
        title = request.POST.get('title')
        description = request.POST.get('description')
        task_status = request.POST.get('task_status')
        estimated_time = request.POST.get('estimated_time')
        employee_id = request.POST.get('employee_id')  # Assuming you have this value
        
        try:
            # Validate and process the data before executing the SQL query
            if title and description and task_status and estimated_time and employee_id:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO task_management_task (title, description, task_status, estimated_time, employee_id_id)
                        VALUES (%s, %s, %s, %s, %s)
                    """, [title, description, task_status, estimated_time, employee_id])

                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failed', 'message': 'Incomplete data'})
        except Exception as e:
            # Handle exceptions or errors
            return JsonResponse({'status': 'failed', 'message': str(e)})

    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'})

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