from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from employee.models import Employees  # Import the Employees model
from task_management.serializers import TaskSerializer
from task_management.models import Task
from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required   

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
    position_list = Position.objects.all()
    context = {
        'page_title':'Positions',
        'positions':position_list,
    }
    return render(request, 'employee_information/positions.html',context)
@login_required
def manage_positions(request):
    position = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            position = Position.objects.filter(id=id).first()
    
    context = {
        'position' : position
    }
    return render(request, 'employee_information/manage_position.html',context)

@login_required
def save_position(request):
    data =  request.POST
    resp = {'status':'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_position = Position.objects.filter(id = data['id']).update(name=data['name'], description = data['description'],status = data['status'])
        else:
            save_position = Position(name=data['name'], description = data['description'],status = data['status'])
            save_position.save()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_position(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Position.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")