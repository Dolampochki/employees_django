from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_employee', views.add_employee, name='add_employee'),
    path('delete_employee', views.delete_employee, name='delete_employee'),
    path('mark_attendance', views.mark_attendance, name='mark_attendance'),
    path('generate_report_employee', views.generate_report_employee, name='generate_report_employee'),
    path('current_month_report', views.current_month_report, name='current_month_report'),
    path('generate_report_late', views.generate_report_late, name='generate_report_late'),
]