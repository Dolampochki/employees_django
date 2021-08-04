from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from . import validators

class Employee(models.Model):
    employee_id = models.IntegerField(validators=[validators.validate_id])
    name = models.CharField(validators=[validators.validate_name], max_length=50)
    phone = models.CharField(validators=[validators.validate_phone], max_length=17)
    age = models.IntegerField(validators=[validators.validate_age])


class EmployeeTimeLog(models.Model):
    employee_id = models.IntegerField(validators=[validators.validate_id])
    date_time = models.DateTimeField()