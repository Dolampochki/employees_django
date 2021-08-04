from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .common import consts
from .forms import EmployeeForm, EmployeeFileForm, SelectEmployee
from . import helpers

def index(request):
    all_employees_list = helpers.get_all_employees_list()
    return render(request, 'employees/index.html', {
        'menu_list': consts.menu_list,
        'all_employees_list': all_employees_list,
        'employee_fields_names': consts.employee_fields_names,
    })

def add_employee(request):
    form_manual = EmployeeForm()
    form_file = EmployeeFileForm()
    added_employees = []
    error = ''
    if request.method == 'POST':
        content = request.POST
        if content.get('employee_id'):
            form_manual = EmployeeForm(content)
            form_values = form_manual.get_content()
            if form_manual.is_valid():
                if not helpers.check_employee_exists(form_values['employee_id']):
                    try:
                        helpers.save_employee(form_values)
                        form_manual = EmployeeForm()
                        added_employees = [form_values]
                    except:
                        error = consts.error_messages['something_wrong']
                else:
                    error = consts.error_messages['employee_exists']
        elif content.get('file_url'):
            form_file = EmployeeFileForm(content)
            form_values = form_file.get_content()
            if form_file.is_valid():
                real_file_url = helpers.get_real_url_if_file_exists(form_values['file_url'])
                if real_file_url:
                    add_to_file = True
                    rows = helpers.get_rows_from_csv_file(real_file_url, add_to_file)
                    if len(rows):
                        try:
                            for row in rows:
                                helpers.save_employee(row)
                            form_file = EmployeeFileForm()
                            added_employees = rows
                        except:
                            error = consts.error_messages['something_wrong']
                    else:
                        error = consts.error_messages['no_valid_rows']
                else:
                    error = consts.error_messages['file_doesnt_exists']


    # return HttpResponseRedirect('/')
    return render(request, 'employees/add_employee.html', {
        'form_manual': form_manual,
        'form_file': form_file,
        'menu_list': consts.menu_list,
        'added_employees': added_employees,
        'employee_fields_names': consts.employee_fields_names,
        'error': error
        })

def delete_employee(request):
    employees_list_len = len(helpers.get_employees_list())
    form_select = SelectEmployee()
    form_file = EmployeeFileForm()
    deleted_employees = []
    error = ''
    if request.method == 'POST':
        content = request.POST
        if content.get('employee_id'):
            form_select = SelectEmployee(content)
            form_values = form_select.get_content()
            try:
                deleted_employee = helpers.delete_employee(form_values['employee_id'])
                deleted_employees = [deleted_employee]
                form_select = SelectEmployee()
                employees_list_len = len(helpers.get_employees_list())
            except:
                error = consts.error_messages['something_wrong']
        elif content.get('file_url'):
            form_file = EmployeeFileForm(content)
            form_values = form_file.get_content()
            if form_file.is_valid():
                real_file_url = helpers.get_real_url_if_file_exists(form_values['file_url'])
                if real_file_url:
                    add_to_file = False
                    rows = helpers.get_rows_from_csv_file(real_file_url, add_to_file)
                    if len(rows):
                        try:
                            for row in rows:
                                helpers.delete_employee(row['employee_id'])
                            form_select = SelectEmployee()
                            form_file = EmployeeFileForm()
                            deleted_employees = rows
                            employees_list_len = len(helpers.get_employees_list())
                        except:
                            error = consts.error_messages['something_wrong']
                    else:
                        error = consts.error_messages['no_valid_rows']
                else:
                    error = consts.error_messages['file_doesnt_exists']

    return render(request, 'employees/delete_employee.html', {
        'form_select': form_select,
        'employees_list_len': employees_list_len,
        'form_file': form_file,
        'menu_list': consts.menu_list,
        'deleted_employees': deleted_employees,
        'employee_fields_names': consts.employee_fields_names,
        'error': error
        })

def mark_attendance(request):
    employees_list_len = len(helpers.get_employees_list())
    form_select = SelectEmployee()
    marked_attendance = []
    error = ''
    if request.method == 'POST':
        content = request.POST
        form_select = SelectEmployee(content)
        form_values = form_select.get_timelog()
        date, time = helpers.get_date_time_fields(form_values['date_time'])
        marked_attendance = [form_values['employee_id'], date, time]
        try:
            helpers.save_attendance(form_values)
        except:
            error = consts.error_messages['something_wrong']

    return render(request, 'employees/mark_attendance.html', {
        'form_select': form_select,
        'employees_list_len': employees_list_len,
        'menu_list': consts.menu_list,
        'attendance_fields_names': consts.attendance_fields_names,
        'marked_attendance': marked_attendance,
        'error': error
        })

def generate_report_employee(request):
    employees_list_len = len(helpers.get_employees_list())
    form_select = SelectEmployee()
    error = ''
    name = ''
    attendances = []
    if request.method == 'POST':
        content = request.POST
        form_select = SelectEmployee(content)
        form_values = form_select.get_content()
        attendances, name = helpers.get_employee_attendances(form_values['employee_id'])
        if not len(attendances):
            error = consts.error_messages['no_reports']
    return render(request, 'employees/generate_report_employee.html', {
        'form_select': form_select,
        'employees_list_len': employees_list_len,
        'menu_list': consts.menu_list,
        'report_fields_names': consts.report_fields_names,
        'error': error,
        'name': name,
        'attendances': attendances
        })

def current_month_report(request):
    error = ''
    attendances, month = helpers.get_current_month_attendances()
    if not len(attendances):
        error = consts.error_messages['no_reports']
    return render(request, 'employees/current_month_report.html', {
        'menu_list': consts.menu_list,
        'report_full_fields_names': consts.report_full_fields_names,
        'error': error,
        'month': month,
        'attendances': attendances
        })

def generate_report_late(request):
    error = ''
    attendances = helpers.get_late_attendances()
    if not len(attendances):
        error = consts.error_messages['no_reports']
    return render(request, 'employees/generate_report_late.html', {
        'menu_list': consts.menu_list,
        'report_full_fields_names': consts.report_full_fields_names,
        'error': error,
        'attendances': attendances
        })
