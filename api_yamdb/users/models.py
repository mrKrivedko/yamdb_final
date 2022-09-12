from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

ROLE = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


def validate_notme(value):
    """Username /me/ зарезервирован, для роутинга users/ во вьюсете."""
    if value == 'me':
        raise ValidationError(
            (_('username is not %(value)s')),
            params={'value': value},
        )


class User(AbstractUser):
    """Переопределяем модель User."""

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        verbose_name=_('username'),
        max_length=150,
        unique=True,
        db_index=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, '
            'digits and @/./+/-/_ only.'
        ),
        validators=[username_validator, validate_notme],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    password = models.CharField(
        verbose_name=_('password'),
        max_length=128,
        blank=True,
        null=True,
        validators=[validate_notme]
    )
    email = models.EmailField(
        verbose_name=_('email address'),
        unique=True
    )
    role = models.CharField(
        verbose_name='Пользовательская роль',
        max_length=16,
        choices=ROLE,
        default='user',
        blank=True,
        help_text='Выберите пользовательскую роль'
    )
    bio = models.TextField(
        verbose_name='Дополнительная информация о пользователе.',
        blank=True,
        help_text='Введите информацию о себе.'
    )
    confirmation_code = models.CharField(
        verbose_name='Код для получения токена',
        max_length=200,
        blank=True,
        null=True,
        help_text='Никому не сообщайте этот код, даже администратору.'
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        if self.role == 'moderator':
            return True
        return False

    @property
    def is_admin(self):
        if self.role == 'admin' or self.is_superuser:
            return True
        return False

    @property
    def is_vip(self):
        if self.is_moderator or self.is_admin:
            return True
        return False

    def __str__(self):
        return self.username
