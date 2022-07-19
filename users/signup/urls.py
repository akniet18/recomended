from django.views.generic import TemplateView
from django.urls import path

from users.signup import views

urlpatterns = [
    path('', views.SignUpView.as_view(), name='signup'),
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify_email'),
    # path('account-confirm-email/<key>', TemplateView.as_view(), name='account_confirm_email'),
]