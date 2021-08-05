
import os.path
import csv
from . import validators
from .models import Employee, EmployeeTimeLog
from datetime import datetime


def get_real_url_if_file_exists(file_url):
    if len(file_url.split('/')) > 1:
        real_file_url = file_url
    else:
        current_dir = os.getcwd()
        real_file_url = current_dir + '/' + file_url
    file_exist = os.path.isfile(real_file_url)
    if not file_exist:
        real_file_url = None
    return real_file_url


def get_rows_from_csv_file(file, add_to_file):
    rows = []
    with open(file) as f:
        reader = csv.reader(f)
        try:
            rows = [return_valid_row(row) for row in reader if validators.row_is_valid(row)]
            rows = return_unique_rows(rows)
            if add_to_file:
                rows = [row for row in rows if not check_employee_exists(row['employee_id'])]
            else:
                rows = [row for row in rows if check_employee_exists(row['employee_id'])]

        except:
            pass
    if not len(rows):
        return None
    else:
        return rows


def return_valid_row(row):
    return {
        'employee_id': int(row[0]),
        'name': row[1],
        'phone': row[2],
        'age': int(row[3])
    }


def return_row_from_object(row_object):
    employee_dict = row_object.__dict__
    del employee_dict['_state']
    del employee_dict['id']
    return employee_dict


def return_unique_rows(rows):
    rows_unique = []
    for row in rows:
        existing_row = next((sub for sub in rows_unique if sub['employee_id'] == row['employee_id']), None)
        if not existing_row:
            rows_unique.append(row)
    return rows_unique


def save_employee(row):
    new_employee = Employee()
    new_employee.__dict__.update(row)
    new_employee.save()


check_employee_exists = lambda employee_id: len(Employee.objects.filter(employee_id = employee_id))
get_employees_list = lambda: [(row.employee_id, str(row.employee_id) + " " + row.name) for row in Employee.objects.all()]


def get_employee_by_id(employee_id):
    employee = None
    empoyees_list = Employee.objects.filter(employee_id = employee_id)
    if len(empoyees_list):
        employee = empoyees_list[0]
    return employee


def delete_employee(employee_id):
    employee = get_employee_by_id(employee_id)
    employee.delete()
    return return_row_from_object(employee)


return_date_time_rows = lambda rows: [[*get_date_time_fields(row.__dict__['date_time'])] for row in rows]


def return_report_rows(rows_objects):
    rows = []
    for row_object in rows_objects:
        name = get_employee_name(row_object.__dict__['employee_id'])
        date, time = get_date_time_fields(row_object.__dict__['date_time'])
        rows.append([row_object.__dict__['employee_id'], name, date, time])
    return rows


def get_date_time_fields(date_time):
    date = date_time.strftime("%d/%m/%Y")
    time = date_time.strftime("%H:%M")
    return date, time


def get_employee_name(employee_id):
    name = str(employee_id)
    employee = get_employee_by_id(employee_id)
    if employee:
        name = employee.__dict__['name'] + ' ' + name
    return name


def save_attendance(row):
    new_attendance = EmployeeTimeLog()
    new_attendance.__dict__.update(row)
    new_attendance.save()


def get_employee_attendances(employee_id):
    if not isinstance(employee_id, int):
        employee_id = int(employee_id)
    employee_attendances = EmployeeTimeLog.objects.filter(employee_id = employee_id)
    employee_attendances = return_date_time_rows(employee_attendances)
    name = get_employee_name(employee_id)
    return employee_attendances, name


def get_current_month_attendances():
    today = datetime.today()
    month = today.strftime("%B %Y")
    attendances = EmployeeTimeLog.objects.filter(date_time__month = today.month, date_time__year = today.year)
    attendances = return_report_rows(attendances)
    return attendances, month

def get_late_attendances():
    attendances = EmployeeTimeLog.objects.all()
    attendances = return_report_rows(attendances)
    attendances = [row for row in attendances if int(row[3].split(':')[0]) > 9 or (int(row[3].split(':')[0]) == 9 and int(row[3].split(':')[1]) >= 30)]
    return attendances

def get_all_employees_list():
    all_employees_list = [return_row_from_object(row) for row in Employee.objects.all()]
    return all_employees_list
