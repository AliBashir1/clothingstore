import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.core import validators


"""
Custom Error message for Alphanumeric, numeric, email address, url fields

"""


def alphabets(string):
    if not string.isalpha():
        raise ValidationError(_("{} is invalid. Please enter alphabets only.".format(string)))
    return string


def alphanumeric(string):
    if string.isnumeric():
        raise ValidationError(_("Please enter combination of numbers and alphabets"))
    return string


def numeric(string):
    if not string.isnumeric():
        raise ValidationError(_("Please enter numbers only"))
    return string


def emailvalidator(string):
    regex = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')

    if not regex.fullmatch(string, 0, len(string)):
        raise ValidationError(_("Please enter valid email"))

    return string


def urlvalidator(value):
    pass

