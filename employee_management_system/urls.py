from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from employee.views import *
from departments.views import *
from task_management.views import *

router = DefaultRouter()
router.register(r'employees', EmployeeModelViewset, basename='employee')
router.register(r'departments',DepartmentModelViewset,basename='department')
router.register(r'tasks',TaskModelViewset,basename='task')


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/",include(router.urls)),
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('login/', auth_views.LoginView.as_view(template_name = 'employee/login.html',redirect_authenticated_user=True), name="login"),
    path('', home, name="home-page"),
    path('userlogin',login_user, name="login-user"),
    path('logout', logoutuser, name="logout"),
    path('employees/', employee_list, name='employee_list'),
    path('departments', departments, name="department-page"),
    path('manage_departments', manage_departments, name="manage_departments-page"),
    path('save_department', save_department, name="save-department-page"),
    path('delete_department', delete_department, name="delete-department"),
    path('tasks',task_list , name="task-page"),
    # path('manage_positions', manage_positions, name="manage_positions-page"),
    # path('save_position', save_position, name="save-position-page"),
    # path('delete_position', delete_position, name="delete-position"),
    path('employees', employees, name="employee-page"),
    path('manage_employees', manage_employees, name="manage_employees"),
    path('save_employee', save_employee, name="save-employee"),
    path('delete_employee', delete_employee, name="delete-employee"),
    path('view_employee', view_employee, name="view-employee"),

]
