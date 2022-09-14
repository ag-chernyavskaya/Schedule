from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import *
from User.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .service import Service
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from schedule_planner_be.settings import SECRET_KEY
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class RegisterView(generics.GenericAPIView):
    """Регистрация пользователя"""
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')

        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        email_body = 'Hi,' + user.first_name + '\n You have been registered at Belhard Academy Schedule Planner. ' \
                                              'Please, follow the link to sign in \n' + absurl
        data = {'email_body': email_body,
                'to_email': [user.email],
                'email_subject': 'Verify your email'}

        Service.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    """Верификация email"""
    queryset = User.objects.all()
    serializer_class = EmailVerificationSerializer
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithm="RS256", options={"verify_signature": False})
            user = User.objects.get(id=payload['user_id'])
            if not user.email_verify:
                user.email_verify = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation link Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    """Логин"""
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    """Сброс пароля"""
    serializer_class = RequestPasswordResetEmailSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://' + current_site + relativeLink
            email_body = 'Hello, \n Use link bellow to reset your password \n' + absurl
            data = {'email_body': email_body,
                    'to_email': [user.email],
                    'email_subject': 'Reset your password'}

            Service.send_email(data)
        return Response({'success': 'We have send you a link to reset your password'},
                        status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    """Проверка токена"""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    serializer_class = SetNewPasswordAPIViewSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'Credentials Valid',
                             'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'Token is not valid, please request a new one'},
                        status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    """Установление нового пароля"""
    serializer_class = SetNewPasswordAPIViewSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
