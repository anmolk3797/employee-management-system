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
    position = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            position = Task.objects.filter(id=id).first()
    
    context = {
        'position' : position
    }
    return render(request, 'employee/manage_tasks.html',context)

@login_required
def save_tasks(request):
    data = request.POST
    resp = {'status': 'failed'}
    
    try:
        if 'id' in data and data['id'].isnumeric() and int(data['id']) > 0:
            task = Task.objects.get(id=data['id'])
            task.title = data.get('title', '')
            task.description = data.get('description', '')
            task.task_status = data.get('task_status', '')  # Ensure this field matches the POST field name
            task.estimated_time = float(data.get('estimated_time', 0))  # Ensure this field matches the POST field name and convert to float
            task.save()
        else:
            employee_id = data.get('employee_id', '')  # Get employee_id from POST data
            # Assuming employee_id is valid and exists in your Employees model
            employee = Employees.objects.get(id=employee_id)
            
            task = Task(
                employee_id=employee,
                title=data.get('title', ''),
                description=data.get('description', ''),
                task_status=data.get('task_status', ''),  # Ensure this field matches the POST field name
                estimated_time=float(data.get('estimated_time', 0))  # Ensure this field matches the POST field name and convert to float
            )
            task.save()
        resp['status'] = 'success'
    except Exception as e:
        resp['status'] = 'failed'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")

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