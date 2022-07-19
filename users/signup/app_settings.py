from django.conf import settings

from rest_framework.permissions import AllowAny
from users.signup.serializers import SignUpSerializer as DefaultSignUpSerializer
from users.utils import import_callable

serializers = getattr(settings, 'REST_AUTH_REGISTER_SERIALIZERS', {})
SignUpSerializer = import_callable('SIGNUP_SERIALIZER', DefaultSignUpSerializer)

def signup_permission_classes():
    permission_classes = [AllowAny, ]
    for klass in getattr(settings, 'REST_AUTH_REGISTER_PERMISSION_CLASSES', tuple()):
        permission_classes.append(import_callable(klass))
    return tuple(permission_classes)