from django.contrib import admin

from .models import Employee, EmployeeTimeLog

admin.site.register(Employee)
admin.site.register(EmployeeTimeLog)
