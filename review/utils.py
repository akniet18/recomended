import io
import os
import sys
import random
import re
from PIL import Image
from django.core.mail import send_mail
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import ugettext_lazy as _
from rest_framework.permissions import BasePermission
from users.models import User
from django.conf import settings

def code_generator(code_length=6):
    allowed_letters = '0123456789'
    return ''.join(random.choice(allowed_letters) for i in range(code_length))


def compress_image(uploaded_image):
    temp = Image.open(uploaded_image)
    outputIOStream = io.BytesIO()
    # temp = temp.resize((300, 400), Image.ANTIALIAS)
    temp = temp.convert('RGB')
    temp.save(outputIOStream, format='JPEG', quality=75)
    outputIOStream.seek(0)
    uploaded_image = InMemoryUploadedFile(outputIOStream, 'ImageField', '%s.jpg', uploaded_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIOStream), None)
    return uploaded_image


def replace_mean_words(text):
    dic = {}
    base_dir = os.path.join(settings.BASE_DIR, 'review')
    with open(f'{base_dir}/lst.txt', 'r') as txt:
        lst = re.split(',', txt.read())
        lst = remove_empty_string_from_array(lst)
        # cleaned_lst = tuple(sorted(set(lst)))
        for i in lst:
            dic.setdefault(i[0], []).append(i)
        temp_text = re.split('[.,!?:; ]', text)
        for i in remove_empty_string_from_array(temp_text):
            if i[0] in dic.keys():
                for idx, elem in enumerate(dic[i[0]]):
                    if i.lower() == elem:
                        text = text.replace(i, f'{i[0]}{"*" * (len(i) - 1)}')
    return text


class ModeratorPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == User.ROLE_MODERATOR:
            return True
        else:
            return False

def remove_empty_string_from_array(arr):
    return [word.strip().lower() for word in arr if len(word) > 1]

def send_email_to_offender(offender, offender_email, secret_code):
    message = _(
        f'Someone has left negative review about you on https://goverdict.com/profile/{offender} . To refute the negative review, enter the code. Your code: {secret_code}')
    subject = _(f'There is some message about you')
    send_mail(subject, message, 'info@goverdict.com', [offender_email])