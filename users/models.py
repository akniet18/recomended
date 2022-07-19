from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)

from rest_framework.authtoken.models import Token as DefaultTokenModel

from locations.models import (Country, City, Region)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError(_("Users must have an email address"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        # user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        # user.role = User.ROLE_ADMINISTRATOR
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    # ROLE_ADMINISTRATOR = 0
    ROLE_MODERATOR = 1
    ROLE_USER = 2
    ROLE_CHOICES = (
        (ROLE_MODERATOR, _('Moderator')),
        (ROLE_USER, _('User'))
    )

    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_NOT_SAY = 2
    GENDER_CHOICES = (
        (GENDER_MALE, _('Male')),
        (GENDER_FEMALE, _('Female')),
        (GENDER_NOT_SAY, _('Rather not say'))
    )

    email = models.EmailField(max_length=255, unique=True)
    role = models.SmallIntegerField(choices=ROLE_CHOICES, default=ROLE_USER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    phone = models.CharField(max_length=15, null=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True,
                                auto_now=False,
                                auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_online = models.DateTimeField(null=True)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES,
                                      null=True, blank=True)

    # avatar = models.ImageField(upload_to=)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_written_by_me_reviews(self):
        return self.reviews_author.all()


    def get_short_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        if self.last_name:
            if self.middle_name:
                return f'{self.last_name} {self.first_name} {self.middle_name}'
            return f'{self.last_name} {self.first_name}'
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
