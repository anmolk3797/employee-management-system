from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import path, include,re_path
from rest_framework.routers import DefaultRouter
from employee.views import *
from departments.views import *
from task_management.views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="EMS API",
      default_version='v1',
      description="Employee Management System Documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="anmolk3797@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



router = DefaultRouter()
router.register(r'employees', EmployeeModelViewset, basename='employee')
router.register(r'departments',DepartmentModelViewset,basename='department')
router.register(r'tasks',TaskModelViewset,basename='task')


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/",include(router.urls)),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

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
    path('manage_tasks', manage_tasks, name="manage_task-page"),
    path('save_tasks', save_tasks, name="save-task-page"),
    path('delete_task', delete_tasks, name="delete-task"),
    path('employees', employees, name="employee-page"),
    path('manage_employees', manage_employees, name="manage_employees"),
    path('save_employee', save_employee, name="save-employee"),
    path('delete_employee', delete_employee, name="delete-employee"),
    path('view_employee', view_employee, name="view-employee"),

]
