from django.urls import path, include
from review import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(prefix='traits', viewset=views.TraitViewSet, base_name='traits')
router.register(prefix='moderator', viewset=views.ReviewModeratorView, base_name='moderator')
urlpatterns = [
    # path('offenders/phone/list/', views.PhoneNumberView.as_view(), name='phone_number_list'),
    path('<id>/delete/', views.ReviewDeleteView.as_view(), name='delete_review'),
    path('offenders/phone/create/', views.PhoneNumberCreate.as_view(), name='phone_number_create'),
    path('offenders/link/create/', views.OffenderLinkCreate.as_view(), name='offender_link_create'),
    path('moderator/list/', views.ReviewModeratorView.as_view({'get': 'list'}), name='list_review'),
    path('cities/', views.CityListView.as_view(), name='city'),
    path('offenders/activity/fields/', views.ActivityFieldListView.as_view(), name='activity_field'),
    path('offenders/professional/area/', views.ProfessionalAreaListView.as_view(), name='prof_area'),
    path('offenders/create/', views.OffenderCreateView.as_view(), name='create_offender'),
    path('offenders/<pk>/', views.OffenderDetailView.as_view(), name='offenders_detail'),
    path('offenders/', views.OffenderListView.as_view(), name='offenders'),
    path('answers/', views.AnswerViewSet.as_view({'get': 'list'}), name='answers'),
    path('create/', views.ReviewCreateView.as_view(), name='reviews_create'),
    path('', views.ReviewListView.as_view(), name='reviews'),
    path('traits/', include(router.urls)),
    path('answers/<pk>/<secure_code>/add/', views.ReviewDetailView.as_view(), name='add_answer'),
    path('answers/create/', views.AnswerCreateView.as_view(), name='create_answer'),
    path('shameless/', views.ShameBoardView.as_view(), name='shame_board'),
    path('shame/of/you/', views.AddToShameBoard.as_view(), name='add_2_shame_board'),
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),
    path('statistics/', views.ReviewAmountView.as_view(), name='statistics'),
    path('advanced/search/', views.OffenderAdvancedSearchView.as_view(), name='advanced_search'),
]


