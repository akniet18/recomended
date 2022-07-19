import re
# from django.core.mail import send_mail
# from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions
from drf_base64.fields import Base64ImageField

from review.models import Review, Answer, Offender, Trait, ShameBoard, Phone, Feedback, OffenderLink
from locations.serializers import CountrySerializer, CitySerializer
from uploads.serializers import UploadSerializer
from professions.models import ActivityField, ProfessionalArea
from .utils import code_generator, replace_mean_words


class PhoneNumberListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('id', 'offender', 'name', 'phone')
        read_only_fields = ('id',)


class OffenderLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffenderLink
        fields = ('id', 'offender', 'link', 'code')
        read_only_fields = ('id',)


class ProfessionalAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalArea
        fields = ('id', 'title', 'title_en')
        read_only_fields = ('id',)

    def create(self, validated_data):
        prof_area, created = ProfessionalArea.objects.get_or_create(**validated_data)
        if not created:
            msg = _(validated_data['title'] + ' already exists')
            raise exceptions.ValidationError(msg)
        return prof_area


class ActivityFieldSerializer(serializers.ModelSerializer):
    professional_area = ProfessionalAreaSerializer(read_only=True)

    class Meta:
        model = ActivityField
        fields = ('id', 'title', 'title_en', 'professional_area')
        read_only_fields = ('id',)

    def create(self, validated_data):
        activity_field, created = ActivityField.objects.get_or_create(**validated_data)
        if not created:
            msg = _(validated_data['title'] + ' already exists')
            raise exceptions.ValidationError(msg)
        return activity_field


class AnswerSerializer(serializers.ModelSerializer):
    proofs = UploadSerializer(source='answer_proof_docs', many=True)
    class Meta:
        model = Answer
        fields = ('id', 'content', 'is_paid', 'created_at', 'proofs')
        read_only_fields = ('id',)


class TraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trait
        fields = ('id', 'name')
        read_only_fields = ('id',)

    def create(self, validated_data):
        # hello = validated_data.pop('name')
        # st = replace_mean_words(hello)
        # print(hello, '<===hhhhh===>', type(st))
        # for word in
        trait, created = Trait.objects.get_or_create(**validated_data)
        if not created:
            msg = _(validated_data['name'] + ' already exists.')
            raise exceptions.ValidationError(msg)
        return trait


class OffenderCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False, use_url=True, max_length=None, default='default.svg')
    traits = serializers.CharField(source='traits.name', max_length=55, allow_blank=True)

    class Meta:
        model = Offender
        fields = ('id', 'city', 'birth_year', 'email', 'traits',
                  'first_name', 'last_name', 'middle_name', 'photo', 'website',
                  'legal_name', 'brand_name', 'type_of_cooperation')
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        # scope_of_cooperation = validated_data.pop('scope_of_cooperation')
        city = validated_data.pop('city')
        birth_year = validated_data.pop('birth_year')
        email = validated_data.pop('email')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        middle_name = validated_data.pop('middle_name')
        legal_name = validated_data.pop('legal_name')
        brand_name = validated_data.pop('brand_name')
        type_of_cooperation = validated_data.pop('type_of_cooperation')
        # activity_field = validated_data.pop('activity_field')
        website = validated_data.pop('website')
        traits = validated_data.pop('traits')
        photo = validated_data.pop('photo')
        # shame_board = validated_data.pop('shame_board')

        new_values = {
            'photo': photo,
            'email': email,
            'city': city,
            'birth_year': birth_year,
            'first_name': first_name,
            'last_name': last_name,
            'middle_name': middle_name,
            'legal_name': legal_name,
            'brand_name': brand_name,
            'type_of_cooperation': type_of_cooperation,
            'website': website,
        }

        if email:
            offender, created = Offender.objects.get_or_create(defaults=new_values, email__iexact=email)
            if created:
                print('created new offender')
        else:
            offender = Offender(**new_values)
        offender.save()  # to get user id
        # censored_lst = replace_mean_words(traits['name'])
        # print(censored_lst)
        # tt = replace_mean_words(traits['name'])
        traits_lst = list(filter(None, re.split('[,.:;!? ]', traits['name'])))
        for trait in traits_lst:
            new_trait, created = Trait.objects.get_or_create(defaults={'name': trait}, name__iexact=trait)
            offender.traits.add(new_trait)

        offender.save()

        return offender


class OffenderPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offender
        fields = ('photo',)


class ReviewSerializer(serializers.ModelSerializer):
    # answer = serializers.CharField(source='review_answer.content')
    # answer_created = serializers.DateTimeField(source='review_answer.created_at')
    # answer_proofs = UploadSerializer(source='answer_proof_docs', many=True)
    answer = AnswerSerializer(source='review_answer')
    proofs = UploadSerializer(source='review_proof_docs', many=True)
    activity_field = ActivityFieldSerializer(read_only=True)
    scope_of_cooperation = ProfessionalAreaSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'content', 'is_confirmed', 'created_at',
                  'paid', 'offender_id', 'get_offender_info',
                  'proofs', 'moderated', 'scope_of_cooperation',
                  'activity_field', 'answer')
        read_only_fields = ('id',)


class OffenderSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    city = CitySerializer(read_only=True)
    type_of_cooperation_display = serializers.CharField(source='get_type_of_cooperation_display')

    class Meta:
        model = Offender
        fields = (
            'id', 'country', 'city', 'birth_year', 'photo',
            'type_of_cooperation_display', 'get_rumor_reviews_count',
            'get_proved_reviews_count', 'first_name', 'last_name',
            'middle_name', 'brand_name', 'legal_name')
        read_only_fields = ('id',)


class AnswerCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # review = ReviewSerializer(read_only=True)
    # proofs = UploadSerializer(source='review_proof_docs', many=True)
    secure_code = serializers.CharField()

    class Meta:
        model = Answer
        fields = ('id', 'content', 'review', 'is_paid', 'secure_code', 'author')
        read_only_fields = ('id',)


class OffenderDetailSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    type_of_cooperation_display = serializers.CharField(source='get_type_of_cooperation_display')
    amount_of_reviews = serializers.IntegerField(source='reviews.count', read_only=True)
    reviews = ReviewSerializer(read_only=True, many=True)
    traits = TraitSerializer(many=True, read_only=True)

    class Meta:
        model = Offender
        fields = ('id', 'city', 'birth_year', 'first_name', 'amount_of_reviews',
                  'last_name', 'middle_name', 'legal_name', 'photo',
                  'brand_name', 'type_of_cooperation', 'type_of_cooperation_display', 'reviews', 'traits',
                  'get_proved_reviews_count', 'get_rumor_reviews_count', 'website')
        read_only_fields = ('id',)


class ReviewCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    moderated = serializers.HiddenField(default=True) # change to false to send to moderator
    paid = serializers.HiddenField(default=True) # change to false to check if paid

    # activity_field = ActivityFieldSerializer(read_only=True)
    # scope_of_cooperation = ProfessionalAreaSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ('id', 'offender', 'content', 'created_at', 'confirm_code', 'paid', 'moderated', 'author', 'payment_uid', 'scope_of_cooperation', 'activity_field')
        read_only_fields = ('id', 'confirm_code', 'author', 'payment_uid')

    def create(self, validated_data):
        offender = validated_data.pop('offender')
        content = validated_data.pop('content')
        author = validated_data.pop('author')
        scope_of_cooperation = validated_data.pop('scope_of_cooperation')
        activity_field = validated_data.pop('activity_field')
        # if settings.DEBUG:
        #     confirm_code = '000000'
        # else:
        confirm_code = code_generator(6)
# <<<<<<< HEAD
# =======
        payment_uid = f'review{code_generator(4)}'
# >>>>>>> 3fca20c59de16ae121b5be895abe1ea879ddf853
        is_paid = validated_data.pop('paid')

        review = Review(offender=offender, content=content, confirm_code=confirm_code, paid=is_paid, author=author, payment_uid=payment_uid, scope_of_cooperation=scope_of_cooperation, activity_field=activity_field, moderated=True)
        review.save()
        return review


class ReviewUpdateSerializer(serializers.ModelSerializer):
    proofs = UploadSerializer(source='review_proof_docs', many=True)
    offender = OffenderDetailSerializer(read_only=True)
    # activity_field = ActivityFieldSerializer(read_only=True)
    # scope_of_cooperation = ProfessionalAreaSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ('id', 'content', 'created_at', 'offender', 'proofs', 'status', 'scope_of_cooperation', 'activity_field')


class ShameBoardSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = ShameBoard
        fields = ('id', 'offender', 'is_paid', 'author')
        read_only_fields = ('id',)


class ShameBoardListSerializer(serializers.ModelSerializer):
    offender = OffenderSerializer(read_only=True)
    class Meta:
        model = ShameBoard
        fields = ('id', 'offender', 'is_paid')
        read_only_fields = ('id',)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'email', 'content')
        read_only_fields = ('id',)
