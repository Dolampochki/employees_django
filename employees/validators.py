from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
import re

phone_regex = r'^\+?1?\d{9,15}$'

id_is_valid = lambda value: 1000 <= value < 10000
full_name_is_valid = lambda value: ''.join(value.split()).isalpha() and len(value.split()) > 1
phone_number_is_valid = lambda value: re.match(phone_regex, value) != None
age_is_valid = lambda value: 18 <= value <= 67
file_url_is_valid = lambda value: value[len(value) - 3:] == 'csv'

def validate_id(value):
    if not id_is_valid(value):
        raise ValidationError(
            _('Employee ID should be decimal, 4 digits'),
            params={'value': value},
        )

def validate_name(value):
    if not full_name_is_valid(value):
        raise ValidationError(
            _('Please input full name'),
            params={'value': value},
        )

validate_phone = RegexValidator(regex=phone_regex, message="Please input a valid phone number")

def validate_age(value):
    if not age_is_valid(value):
        raise ValidationError(
            _('Employee can be 18-67 years old'),
            params={'value': value},
        )


def validate_file_url(value):
    if not file_url_is_valid(value):
        raise ValidationError(
            _('It must be csv file'),
            params={'value': value},
        )

def row_is_valid(row):
    if len(row) != 4 or not row[0].isdecimal() or not row[3].isdecimal():
        return False
    return id_is_valid(int(row[0])) and \
        full_name_is_valid(row[1]) and \
        phone_number_is_valid(row[2]) and \
        age_is_valid(int(row[3]))