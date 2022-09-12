from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from users.models import User


class SignupSerialiser(serializers.ModelSerializer):
    """Сериализатор для регистрации."""

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (User.USERNAME_FIELD,)

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail(_("cannot_create_user"))
        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
        return user


class CreateUserSerialiser(serializers.ModelSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        model = User
        fields = (
            tuple(User.REQUIRED_FIELDS)
            + (
                User.USERNAME_FIELD,
                'first_name',
                'last_name',
                'bio',
                'role'
            )
        )

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail(_("cannot_create_user"))

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
        return user


class GetUserSerializer(serializers.ModelSerializer):
    """Сериализатор для получения пользователя."""

    class Meta:
        model = User
        fields = User.USERNAME_FIELD


class TokenCreateSerialiser(serializers.Serializer):
    """Сериализатор для создания токена."""

    username = serializers.CharField(
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=200,
        required=True
    )

    default_error_messages = {
        'invalid_conf_code': 'Sorry, bad confirmation code',
    }

    def validate(self, attrs):
        """Валидируем введеный код."""

        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            self.fail('invalid_conf_code')
        return attrs
