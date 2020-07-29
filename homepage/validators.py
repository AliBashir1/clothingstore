import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.core import validators


"""
Custom Error message for Alphanumeric, numeric, email address, url fields
These a very basic simple validation right now. Main purpose of it to be more dynamic and scalable in future.
"""


def alphabets(string):

    string = string.strip()
    if not all(x.isalpha() or x.isspace() for x in string):
        raise ValidationError(_('"{}" is invalid. Please enter alphabets only.'.format(string)))
    return string


def alphanumeric(string):
    if not all(x.isalpha() or x.isnumeric() or x.isspace() for x in string):
        raise ValidationError(_('"{}" is invalid. Please enter combination of numbers and alphabets. No dots or special character allowed'.format(string)))
    return string


def alphanumspecial(string):
    if not all(x.isalpha() or x.isnumeric() or x.isspace() or x in ['.', ',', '#'] for x in string):
        raise ValidationError(_('"{}" is invalid. only numbers, alphabets, comma, hashtag and dots are allowed '.format(string)))

    return string


def numeric(number):
    # todo this needs work
    if number < 0:
        raise ValidationError(_('"{}" is invalid, Please enter positive number'.format(number)))
    return number


def emailvalidator(string):
    # regex will send False for emails like some.com someame@shahe

    email_regex = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')

    if not email_regex.fullmatch(string, 0, len(string)):
        raise ValidationError(_("Please enter valid email"))

    return string


def httpurlvalidator(string):
    """
    This method will only accept url start with www.something.com or http:// or https://. it wont work for ftp ftps since
    we dont need ftp link
    :param string:
    :return:
    """
    http_regex = re.compile(r'((((ht){1}tp(s?)://)|(www\.))[-a-zA-Z0-9@:%_\+.~#?&//=]+)')
    ftp_regex = re.compile(r'((((ft|ht){1}tp(s?)://)|(www\.))[-a-zA-Z0-9@:%_\+.~#?&//=]+)')

    if not http_regex.fullmatch(string, 0 , len(string)):
        raise ValidationError(_("Please enter valid website - starting with http or https or www.  "))

    return string


def min_value(number):
    if number < 1:
        raise ValidationError(_('"{}" is invalid. Please number higher or equal to 1.'.format(number)))
    return number