from django.db import models
from django.core.mail import send_mail
from django.contrib.postgres.indexes import BrinIndex
from django.utils.translation import ugettext_lazy as _
from uploads.utils import user_photo_path
from review.utils import compress_image
from locations.models import Country, City, Region
from professions.models import ProfessionalArea, ActivityField
from users.models import User
from django.conf import settings
# <<<<<<< HEAD
from .utils import replace_mean_words
from .signals import payment_completed, payment_process
# =======
from .utils import replace_mean_words, send_email_to_offender
# >>>>>>> 3fca20c59de16ae121b5be895abe1ea879ddf853


class Trait(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('Name'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = (
            BrinIndex(fields=['created_at']),
        )
        ordering = ('-created_at',)

    def __str__(self):
        return '{} traits'.format(self.name)

    def save(self, *args, **kwargs):
        self.name = replace_mean_words(self.name)
        super(Trait, self).save(*args, **kwargs)


class Offender(models.Model):
    EMPLOYEE = 0
    EMPLOYER = 1
    CONTRACTOR = 2
    CUSTOMER = 3
    PARTNER = 4

    TYPE_OF_COOPERATION = (
        (EMPLOYEE, _('Employee')),
        (EMPLOYER, _('Employer')),
        (CONTRACTOR, _('Contractor')),
        (CUSTOMER, _('Customer')),
        (PARTNER, _('Partnership')),
    )

    # common fields
    type_of_cooperation = models.SmallIntegerField(choices=TYPE_OF_COOPERATION)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    # scope_of_cooperation = models.ForeignKey(ProfessionalArea, blank=True, null=True, on_delete=models.SET_NULL)
    # activity_field = models.ForeignKey(ActivityField, blank=True, null=True, on_delete=models.SET_NULL)
    # phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(verbose_name=_('User photo or brand logo'),
                              upload_to=user_photo_path, null=True, blank=True)

    # user fields
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    birth_year = models.CharField(max_length=5, blank=True, null=True)
    traits = models.ManyToManyField(Trait, related_name='offenders', blank=True)

    # company fields
    legal_name = models.CharField(max_length=255, blank=True, null=True)
    brand_name = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)

    # shame_board = models.BooleanField(default=False)

    class Meta:
        indexes = (
            BrinIndex(fields=['created_at']),
        )
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.email)

    def get_proved_reviews_count(self):
        return self.reviews.filter(status=True).count()

    def get_rumor_reviews_count(self):
        return self.reviews.filter(status=False).count()

    def get_full_name(self):
        if self.first_name:
            if self.last_name:
                return '{} {}'.format(self.first_name, self.last_name)
            return self.first_name
        elif self.last_name:
            return self.last_name
        elif self.legal_name:
            if self.brand_name:
                return '{} {}'.format(self.brand_name, self.legal_name)
            return self.legal_name
        elif self.brand_name:

            return self.brand_name

    def save(self, *args, **kwargs):
        try:
            if self.photo:
                self.photo = compress_image(self.photo)
# <<<<<<< HEAD
                print('I have worked')
        except Exception as e:
            print(e, 'Not')
# =======
                # print('I ahve worked')
        except Exception as e:
            print('Not')
# >>>>>>> 3fca20c59de16ae121b5be895abe1ea879ddf853
        super(Offender, self).save(*args, **kwargs)


class Review(models.Model):
    STATUS_RELIABLE = True
    STATUS_RUMORS = False
    STATUS_CHOICES = (
        (STATUS_RELIABLE, _('Reliable')),
        (STATUS_RUMORS, _('Rumors')),
    )

    offender = models.ForeignKey(Offender, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField(
        verbose_name=_('Review content')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    confirm_code = models.SlugField()
    scope_of_cooperation = models.ForeignKey(ProfessionalArea, blank=True, null=True,
                                             on_delete=models.SET_NULL,
                                             related_name='review_scope_cooperation')
    activity_field = models.ForeignKey(ActivityField, blank=True, null=True,
                                       on_delete=models.SET_NULL)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, editable=False,
                                      default=STATUS_RUMORS)
    moderator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                  blank=True, related_name='review_moderator')
    moderated = models.BooleanField(default=False)
    # is_paid = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
# <<<<<<< HEAD
    # payment_uid = models.CharField(max_length=25, null=True, blank=True)
    
# =======
    payment_uid = models.CharField(max_length=25, null=True, blank=True)
# >>>>>>> 3fca20c59de16ae121b5be895abe1ea879ddf853
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='reviews_author')

    class Meta:
        indexes = (
            BrinIndex(fields=['created_at']),
        )
        ordering = ('-created_at',)

    def __str__(self):
        return self.content

    def get_proof_docs(self):
        return self.review_proof_docs

    def get_offender_info(self):
        return self.offender.get_full_name()

    def offender_id(self):
        return self.offender.id

    def save(self, *args, **kwargs):
        self.content = replace_mean_words(self.content)
        if self.moderated is False and self.get_proof_docs():
            self.moderator = User.objects.filter(role=User.ROLE_MODERATOR)[0]
        super(Review, self).save(*args, **kwargs)
        # if self.offender.email:
            # send_email_to_offender(offender_email=self.offender.email, secret_code=self.confirm_code, offender_id=self.offender.id)


class Answer(models.Model):
    content = models.TextField(
        max_length=1024,
        verbose_name=_('Answer content')
    )
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='review_answer')
    secure_code = models.SlugField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='answer_author')

    class Meta:
        indexes = (
            BrinIndex(fields=['created_at']),
        )
        ordering = ('-created_at',)

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
        self.content = replace_mean_words(self.content)
        super(Answer, self).save(*args, **kwargs)


class ShameBoard(models.Model):
    offender = models.ForeignKey(Offender,
                                 on_delete=models.CASCADE, related_name='offender_shame')
    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='shame_board_author')

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )

    def __str__(self):
        return 'Paid for shame board? {}'.format(self.is_paid)


class Phone(models.Model):
    HOME = 0
    WORK = 1
    MOBILE = 2
    MAIN = 3
    HOME_FAX = 4
    WORK_FAX = 5
    PAGER = 6
    OTHER = 7
    PHONE_NUMBER_CHOICES = (
        (HOME, _('Home')),
        (WORK, _('Work')),
        (MOBILE, _('Mobile')),
        (MAIN, _('Main')),
        (HOME_FAX, _('Home fax')),
        (WORK_FAX, _('Work fax')),
        (PAGER, _('Pager')),
        (OTHER, _('Other'))
    )
    offender = models.ForeignKey(Offender, on_delete=models.CASCADE, related_name='offender_phone')
    name = models.SmallIntegerField(choices=PHONE_NUMBER_CHOICES, default=WORK)
    phone = models.CharField(max_length=15, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = (
            BrinIndex(fields=['added_at']),
        )
        ordering = ('-added_at',)

    def __str__(self):
        return 'phone number is {}'.format(self.phone)


class Feedback(models.Model):
    email = models.CharField(max_length=255)
    content = models.TextField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = (
            BrinIndex(fields=['created_at']),
        )
        ordering = ('-created_at',)

    def __str__(self):
        return '{}'.format(self.email)


    def save(self, *args, **kwargs):
        super(Feedback, self).save(*args, **kwargs)
# <<<<<<< HEAD
        send_mail(_('Feedback from {}'.format(self.email)),
                  self.content,
                  self.email, ['support@goverdict.com'])


class PaymentYM(models.Model):
    class ORDER_TYPE:
        ANSWER = 0
        DELETION = 1
        REVIEW = 2
        REVIEW_WITH_BENEFITS = 3
        SHAME_BOARD = 4

        CHOICES = (
            (ANSWER, _('Answer')),
            (DELETION, _('Deletion')),
            (REVIEW, _('Review')),
            (REVIEW_WITH_BENEFITS, _('Review and Shame board')),
            (SHAME_BOARD, _('Shame board')),
        )

    class STATUS:
        PROCESSED = 0
        SUCCESS = 1
        FAIL = 2

        CHOICES = (
            (PROCESSED, _('Processed')),
            (SUCCESS, _('Success')),
            (FAIL, _('Fail'))
        )

    class PAYMENT_TYPE:
        PC = 'PC'
        AC = 'AC'
        MC = 'MC'
        WM = 'WM'
        MA = 'MA'
        QW = 'QW'

        CHOICES = (
            (PC, _('Кошелек Яндекс.Деньги')),
            (AC, _('Банковская карта')),
            # (MC, _('Счет мобильного телефона')),
            (WM, _('Кошелек WebMoney')),
            # (MA, _('MasterPass')),
            (QW, _('QIWI Wallet')),
        )

    class CURRENCY:
        RUB = 643
        TEST = 10543

        CHOICES = (
            (RUB, _('Rubles')),
            (TEST, _('Test')),
        )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             blank=True, null=True,
                             verbose_name=_('User'),
                             on_delete=models.CASCADE,
                             related_name='payments_author')
    created_at = models.DateTimeField(_('Created time'), auto_now_add=True)
    order_type = models.SmallIntegerField(_('Payment for'), default=ORDER_TYPE.REVIEW, choices=ORDER_TYPE.CHOICES)
    amount = models.DecimalField(_('Total amount for payment'), max_digits=15, decimal_places=2)
    currency = models.PositiveIntegerField(_('Currency'), default=CURRENCY.TEST, choices=CURRENCY.CHOICES)
    status = models.CharField(_('Status'), max_length=15, choices=STATUS.CHOICES, default=STATUS.PROCESSED)
    payment_type = models.CharField(_('Payment type'),
                                    max_length=2,
                                    default=PAYMENT_TYPE.AC,
                                    choices=PAYMENT_TYPE.CHOICES)

    @property
    def is_paid(self):
        return self.status == self.STATUS.SUCCESS

    def send_signals(self):
        status = self.status
        if status == self.STATUS.PROCESSED:
            payment_process.send(sender=self)
        if status == self.STATUS.SUCCESS:
            payment_completed.send(sender=self)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        return '''Payment id = {}, user = {}, 
                  order_type = {}, payment_amount = {}, 
                  currency = {}'''.format(self.id,
                                          self.user,
                                          self.order_type,
                                          self.amount,
                                          self.currency)


class OffenderLink(models.Model):
    class CODE:
        LINKEDIN = 0
        FACEBOOK = 1
        VK = 2
        HH = 3
        INSTAGRAM = 5
        TWITTER = 6
        TELEGRAM = 7
        VIBER = 8
        DISCORD = 9
        OTHER = 10

        CHOICES = (
            (LINKEDIN, _('LinkedIn')),
            (FACEBOOK, _('Facebook')),
            (VK, _('VK')),
            (HH, _('HeadHunter')),
            (INSTAGRAM, _('Instagram')),
            (TWITTER, _('Twitter')),
            (TELEGRAM, _('Telegram')),
            (VIBER, _('Viber')),
            (DISCORD, _('Discord')),
            (OTHER, _('Other'))
        )

    offender = models.ForeignKey(Offender, on_delete=models.CASCADE, related_name='offender_link')
    link = models.URLField(max_length=255, null=True, blank=True)
    code = models.SmallIntegerField(_('Link code'), choices=CODE.CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = (
            BrinIndex(fields=['created_at']),
        )
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.link}'
# =======
        send_mail(_('Feedback from {}'.format(self.email)), self.content, self.email, ['support@goverdict.com'])


# class Payment(models.Model):
# >>>>>>> 3fca20c59de16ae121b5be895abe1ea879ddf853
