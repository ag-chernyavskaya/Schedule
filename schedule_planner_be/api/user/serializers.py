from django.core.validators import RegexValidator
from rest_framework import serializers
from User.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class RegisterSerializer(serializers.ModelSerializer):
    """Добавление пользователя"""
    password = serializers.CharField(label='Password', validators=[
        RegexValidator(
            regex="^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8}$",
            message=_('Invalid password'),
            code=_('invalid_password')
        )], help_text=_('Password should have only 8 characters, '
                        'at least one digit, one upper case letter and one lower case letter'),
                                      write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'role', 'password')

    def create(self, validated_data):
        """Создание пользователя, сохранение предоставленного пароля в хешированном формате"""
        user = super(RegisterSerializer, self).create(validated_data)
        user.set_password(self.validated_data["password"])
        user.save()
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(label='Password', validators=[
        RegexValidator(
            regex="^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8}$",
            message=_('Invalid password'),
            code=_('invalid_password')
        )], help_text=_('Password should have only 8 characters, '
                        'at least one digit, one upper case letter and one lower case letter'),
                                     write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)
        # if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
        #     raise AuthenticationFailed(
        #         detail='Please continue your login using' + filtered_user_by_email[0].auth_provider
        #     )
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.email_verify:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'tokens': user.tokens
        }


class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ['email']


class SetNewPasswordAPIViewSerializer(serializers.Serializer):
    password = serializers.CharField(label='Password', validators=[
        RegexValidator(
            regex="^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8}$",
            message=_('Invalid password'),
            code=_('invalid_password')
        )], help_text=_('Password should have only 8 characters, '
                        'at least one digit, one upper case letter and one lower case letter'),
                                     write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)

