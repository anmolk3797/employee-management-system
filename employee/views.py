from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from employee.serializers import EmployeeSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required   
from django.http import HttpResponse
from django.shortcuts import redirect
import json
from employee.models import Employees
from departments.models import Department
from task_management.models import Task
from django.db import connection
import base64
from django.core.files.base import ContentFile




class EmployeeModelViewset(viewsets.ModelViewSet):
    # queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM  employee_Employees")
            results = cursor.fetchall()

        # Assuming your results follow the same structure as the model fields,
        # you can manually create instances of YourModel from the raw results.
        queryset = [Employees(*result) for result in results]

        return queryset

#login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#logout
def logoutuser(request):
    logout(request)
    return redirect('/')

#home page
@login_required
def home(request):
    context = {
        'page_title':'Home',
        'employees':Employees,
        'total_department':len(Department.objects.all()),
        'total_task':len(Task.objects.all()),
        'total_employee':len(Employees.objects.all()),
    }
    return render(request, 'employee/home.html',context)



def employee_list(request):
    employees = Employees.objects.all()
    return render(request, 'employee/employees.html', {'employees': employees})


@login_required
# Employees
def employees(request):
    employee_list = Employees.objects.all()
    context = {
        'page_title':'Employees',
        'employees':employee_list,
    }
    return render(request, 'employee/employees.html',context)
@login_required
def manage_employees(request):
    employee = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()
    context = {
        'employee' : employees,
    }
    return render(request, 'employee/manage_employee.html',context)

@login_required
def save_employee(request):
    data =  request.POST
    resp = {'status':'failed'}
    if (data['id']).isnumeric() and int(data['id']) > 0:
        check  = Employees.objects.exclude(id = data['id']).filter(code = data['code'])
    else:
        check  = Employees.objects.filter(code = data['code'])

    if len(check) > 0:
        resp['status'] = 'failed'
        resp['msg'] = 'Code Already Exists'
    else:
        try:
            if data['id'].isnumeric() and int(data['id']) > 0:
                save_employee = Employees.objects.filter(id=data['id']).update(
                    code=data['code'],
                    firstname=data['firstname'],
                    middlename=data['middlename'],
                    lastname=data['lastname'],
                    dob=data['dob'],
                    gender=data['gender'],
                    contact=data['contact'],
                    email=data['email'],
                    address=data['address'],
                    date_hired=data['date_hired'],
                    salary=data['salary'],
                    status=data['status']
                )
            else:
                save_employee = Employees(
                    code=data['code'],
                    firstname=data['firstname'],
                    middlename=data['middlename'],
                    lastname=data['lastname'],
                    dob=data['dob'],
                    gender=data['gender'],
                    contact=data['contact'],
                    email=data['email'],
                    address=data['address'],
                    date_hired=data['date_hired'],
                    salary=data['salary'],
                    status=data['status']
                )
                # Handle file upload
                if 'document' in data:
                    document_content = base64.b64decode(data['document'])
                    save_employee.document.save(data['code'] + '_document.pdf', ContentFile(document_content), save=False)
                save_employee.save()
            resp['status'] = 'success'
        except Exception as e:
            resp['status'] = 'failed'
            print(e)
            print(json.dumps({
                "code": data['code'],
                "firstname": data['firstname'],
                "middlename": data['middlename'],
                "lastname": data['lastname'],
                "dob": data['dob'],
                "gender": data['gender'],
                "contact": data['contact'],
                "email": data['email'],
                "address": data['address'],
                "date_hired": data['date_hired'],
                "salary": data['salary'],
                "status": data['status']
            }))
        return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_employee(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Employees.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_employee(request):
    employee = {} 
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()
    context = {
        'employee' : employees,
    }
    return render(request, 'employee/view_employee.html',context)