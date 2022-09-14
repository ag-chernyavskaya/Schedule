from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('confirm_email/', TemplateView.as_view(template_name='registration/confirm_email.html'),
         name='confirm_email'),
    path('verify_email/<uidb64>/<token>/', views.EmailVerify.as_view(),
         name="verify_email",
    ),
    path(
        'invalid_verify/', TemplateView.as_view(
            template_name='registration/invalid_verify.html'
        ),
        name='invalid_verify'
    ),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         views.MyPasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('send_repeat_message/', views.SendRepeatMessage.as_view(), name='send_repeat_message'),
    path(
        'complete_verify_email/', TemplateView.as_view(
            template_name='registration/complete_verify_email.html'
        ),
        name='complete_verify_email'),
    path(
        'send_message/', TemplateView.as_view(
            template_name='registration/send_repeat_message.html'
        ),
        name='send_message')
]