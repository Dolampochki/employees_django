from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from . import validators, helpers
from datetime import datetime

class EmployeeForm(forms.Form):
    employee_id = forms.IntegerField(validators=[validators.validate_id])
    name = forms.CharField(validators=[validators.validate_name], max_length=50)
    phone = forms.CharField(validators=[validators.validate_phone], max_length=17)
    age = forms.IntegerField(validators=[validators.validate_age])
    def get_content(self):
        return {
            'employee_id': self['employee_id'].value(),
            'name': self['name'].value(),
            'phone': self['phone'].value(),
            'age': self['age'].value()
        }

class EmployeeFileForm(forms.Form):
    file_url = forms.CharField(validators=[validators.validate_file_url], max_length=300)
    def get_content(self):
        return {
            'file_url': self['file_url'].value()
        }

# creating a form
class SelectEmployee(forms.Form):
    employee_id = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(SelectEmployee,self).__init__(*args, **kwargs)
        employees_list = helpers.get_employees_list()
        self.fields['employee_id'].choices = employees_list
    def get_content(self):
        return {
            'employee_id': int(self['employee_id'].value())
        }
    def get_timelog(self):
        return {
            'employee_id': int(self['employee_id'].value()),
            'date_time': datetime.today()
        }

