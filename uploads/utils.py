import uuid
import os
from datetime import datetime
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework.serializers import ValidationError


def upload_file_path(instance, filename):
    ext = filename.split('.')[-1]
    if instance.review:
        filename = f'reviews/{uuid.uuid4().hex}.{ext}'
    else:
        filename = f'answers/{uuid.uuid4().hex}.{ext}'
    current_date = f'{datetime.today().strftime("%d_%m_%Y")}'
    return f'documents/{current_date}/{filename}'


def user_photo_path(instance, filename):
    today = datetime.today()
    if instance.email:
         folder_name = f'offenders/photo/{instance.email}/{today.year}/{today.month}/{today.day}/{filename}'
    elif instance.get_full_name():
        folder_name = f'offenders/photo/{instance.get_full_name()}/{today.year}/{today.month}/{today.day}/{filename}'
    else:
        folder_name = f'offenders/photo/{today.year}/{today.month}/{today.day}/{filename}'
    return folder_name


def validate_file_extension(uploaded_file):
    # print(dir(uploaded_file))
    # print(uploaded_file.content_type)
    # print(uploaded_file.name)
    ext = uploaded_file.name.split('.')[-1]
    print(ext)
    valid_extensions = ['pdf', 'doc', 'docx', 'png', 'jpeg', 'jpg']
    if not ext.lower() in valid_extensions:
        msg = _('File not supported')
        raise ValidationError(msg)


def validate_file_size(temp_file):
    size = temp_file.size / 1048576
    if size > settings.FILE_MAX_UPLOAD_SIZE:
        msg = _('You have uploaded greater than 200 mb file')
        raise ValidationError(msg)
