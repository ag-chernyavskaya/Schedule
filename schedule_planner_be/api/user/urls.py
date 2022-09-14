from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login-api'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('email_verify/', views.VerifyEmail.as_view(), name='email-verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('request_reset_email/', views.RequestPasswordResetEmail.as_view(),
         name='request-reset-email'),
    path('password_reset/<uidb64>/<token>/', views.PasswordTokenCheckAPI.as_view(),
         name='password-reset-confirm'),
    path('password_reset_complete/', views.SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')
]
