menu_list = [
    {
        'name': 'Home',
        'page': '/'
    },
    {
        'name': 'Add employee',
        'page': 'add_employee'
    },
    {
        'name': 'Delete employee',
        'page': 'delete_employee'
    },
    {
        'name': 'Mark attendance',
        'page': 'mark_attendance'
    },
    {
        'name': 'Generate attendance report',
        'page': 'generate_report_employee'
    },
    {
        'name': 'Print a report for current month',
        'page': 'current_month_report'
    },
    {
        'name': 'Print a report for all late employees',
        'page': 'generate_report_late'
    }
]

employee_fields_names = ['Employee ID', 'Name', 'Phone', 'Age']
attendance_fields_names = ['Employee ID', 'Date', 'Time']
report_fields_names = ['Date', 'Time']
report_full_fields_names = ['Employee ID', 'Name', 'Date', 'Time']

error_messages = {
    'file_doesnt_exists': "Given file doesn't exists",
    'no_valid_rows': 'File has no valid rows (data is wrong or all employees are already exists)',
    'employee_exists': 'Employee with this ID already exists',
    'something_wrong': 'Something wrong with Database update',
    'no_reports': 'No reports for'
}