from django.urls import path, include
from allauth.account.views import ConfirmEmailView
from users import views

urlpatterns = [
    path('signup/account-email-verification-sent/', views.null_view, name='account_email_verification_sent'),
    path('signup/account-confirm-email/<key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('signup/complete/', views.complete_view, name='account_confirm_complete'),
    # path('password-reset/confirm/<uidb64>/', views.null_view, name='password_reset_confirm'),
    path('signup/', include('users.signup.urls')),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.UserDetailsView.as_view(), name='me'),
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    # path('', include('rest_auth.urls')),
]