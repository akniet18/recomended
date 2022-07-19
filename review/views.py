import datetime
from django.db.models import Q
from django.http import Http404
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework.pagination import CursorPagination
from rest_framework import viewsets, generics, mixins, filters
from rest_framework.response import Response
from rest_framework import permissions, status, exceptions

from professions.models import ActivityField, ProfessionalArea
from locations.models import City
from locations.serializers import CitySerializer
# <<<<<<< HEAD
from review.models import Offender, Review, Answer, Trait, ShameBoard, Phone, Feedback, OffenderLink
# =======
from review.models import Offender, Review, Answer, Trait, ShameBoard, Phone, Feedback
# >>>>>>> 3fca20c59de16ae121b5be895abe1ea879ddf853
from review.serializers import (OffenderDetailSerializer, ReviewUpdateSerializer,
                                OffenderSerializer, ReviewSerializer, ShameBoardSerializer,
                                AnswerSerializer, OffenderCreateSerializer, ShameBoardListSerializer,
                                ReviewCreateSerializer, PhoneNumberListSerializer, OffenderLinkSerializer,
                                ProfessionalAreaSerializer, ActivityFieldSerializer,
                                TraitSerializer, AnswerCreateSerializer, FeedbackSerializer)

from .utils import code_generator, ModeratorPermissions, send_email_to_offender


class CursorSetPagination(CursorPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    ordering = '-created_at'





# def send_email(offender_id, secret_code):
#     offender = Offender.objects.get(id=offender_id)
#     if offender.email:
#         send_mail('Tsss...', f'Hey, wazzzzzzzaaaap! Somebody left review about you. Check it out! your code to write answer is {secret_code}', 'from@mail.ru', [offender.email])
#     else:
#         pass


class AnswerViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Answer.objects.all()
        serializer = AnswerSerializer(queryset, many=True)
        return Response(serializer.data)


class OffenderAdvancedSearchView(generics.ListAPIView):
    serializer_class = OffenderSerializer
    queryset = Offender.objects.all()
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('first_name', 'last_name',
                     'middle_name', 'email',
                     'birth_year', 'legal_name',
                     'brand_name', 'type_of_cooperation')

    def get_queryset(self):
        return self.queryset.all()


class OffenderListView(generics.ListAPIView):
    pagination_class = CursorSetPagination
    serializer_class = OffenderSerializer
    queryset = Offender.objects.all()
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name',
                     'middle_name', 'email',
                     'birth_year', 'legal_name',
                     'brand_name')

    def get_queryset(self):
        return self.queryset.all()


class OffenderDetailView(generics.RetrieveAPIView):
    # lookup_field = 'first_name'
    serializer_class = OffenderDetailSerializer
    queryset = Offender.objects.all()
    permission_classes = (permissions.AllowAny,)


class OffenderCreateView(generics.CreateAPIView):
    serializer_class = OffenderCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Offender.objects.all()


class ReviewListView(generics.ListAPIView):
    pagination_class = CursorSetPagination
    serializer_class = ReviewSerializer
    queryset = Review.objects.filter(Q(paid=True) & Q(moderated=True))
    permission_classes = (permissions.AllowAny,)


class ReviewModeratorView(viewsets.ViewSet):
    # serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated, ModeratorPermissions)
    allowed_methods = ('PUT', 'GET')

    def list(self, request):
        # print(request)
        queryset = Review.objects.filter(Q(paid=True) & Q(moderator=self.request.user) & Q(moderated=False))
        serializer = ReviewUpdateSerializer(queryset, many=True)
        return Response(serializer.data)


class ReviewDetailView(generics.RetrieveAPIView):
    # lookup_field = 'id'
    serializer_class = ReviewSerializer
    queryset = Review.objects.filter(Q(paid=True) & Q(moderated=True))
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        secure_code = kwargs['secure_code']
        instance = self.get_object()
        # print(dir(instance))
        # print(instance.review_answer)
        if secure_code == instance.confirm_code:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return exceptions.MethodNotAllowed(detail='Forbidden', code=status.HTTP_403_FORBIDDEN)


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        # print(request.data)
        response = super(ReviewCreateView, self).create(request, *args, **kwargs)
        try:
            offender = Offender.objects.get(id=response.data['offender'])
        except ValueError:
            offender = None
        if offender.email:
            send_email_to_offender(offender=offender.id, offender_email=offender.email,
                                   secret_code=response.data['confirm_code'])
        return response


class AnswerCreateView(generics.CreateAPIView):
    serializer_class = AnswerCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        try:
            review = Review.objects.get(id=int(request.data['review']))
        except ValueError:
            print('Value error')
            review = None

        if review:
            if review.confirm_code == request.data['secure_code']:
                response = super(AnswerCreateView, self).create(request, *args, **kwargs)
                review.confirm_code = code_generator(23)
                review.save()
            else:
                msg = _('Something went wrong')
                return exceptions.PermissionDenied(detail=msg,
                                                   code=status.HTTP_403_FORBIDDEN)
        else:
            msg = _('review doesnt exists')
            return exceptions.NotFound(detail=msg, code=status.HTTP_404_NOT_FOUND)
            # return Response({'err': msg, 'code': status.HTTP_404_NOT_FOUND})
        return response


class ActivityFieldListView(generics.ListAPIView):
    serializer_class = ActivityFieldSerializer
    queryset = ActivityField.objects.all()
    permission_classes = (permissions.AllowAny,)


class ProfessionalAreaListView(generics.ListAPIView):
    serializer_class = ProfessionalAreaSerializer
    queryset = ProfessionalArea.objects.all()
    permission_classes = (permissions.AllowAny,)


class TraitViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin):
    permission_classes = (permissions.AllowAny,)
    queryset = Trait.objects.all()
    serializer_class = TraitSerializer

    def perform_create(self, serializer):
        serializer.save()


class CityListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = City.objects.all()
    serializer_class = CitySerializer


class ShameBoardView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = ShameBoard.objects.all().order_by('-created')[:12]
    serializer_class = ShameBoardListSerializer


class AddToShameBoard(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ShameBoardSerializer
    queryset = ShameBoard.objects.all()


class PhoneNumberCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PhoneNumberListSerializer
    queryset = Phone.objects.all()


class OffenderLinkCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OffenderLinkSerializer
    queryset = OffenderLink.objects.all()


class ReviewDeleteView(generics.DestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'
    queryset = Review.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if self.request.user == instance.author:
                self.perform_destroy(instance)
                return Response({'msg': _('OK'), 'status': status.HTTP_200_OK})
            else:
                return exceptions.MethodNotAllowed(detail=_('You are not author of this review'),
                                                   code=status.HTTP_403_FORBIDDEN)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class FeedbackView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()


class ReviewAmountView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def list(self, request, *args, **kwargs):
        last_week = timezone.now().date() - datetime.timedelta(days=7)
        per_week = self.queryset.filter(created_at__gt=last_week).count()
        per_day = self.queryset.filter(created_at__gt=timezone.now().date()).count()
        total = self.queryset.all().count()
        return Response(
            {
                'day': per_day,
                'week': per_week,
                'total': total
            }
        )
