from datetime import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class Genre(models.Model):
    """Модель для жанров."""

    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256,
        db_index=True,
        help_text='Обязательное поле. Введите название жанра'
    )
    slug = models.SlugField(
        verbose_name='Уникальное имя жанра',
        unique=True,
        help_text='Обязательное поле. Только латиница.'
    )

    REQUIRED_FIELDS = ['name', 'slug']

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель для категорий."""

    name = models.CharField(
        verbose_name='Название категории',
        max_length=256,
        db_index=True,
        help_text='Обязательное поле. Введите название категории'
    )
    slug = models.SlugField(
        verbose_name='Название категории',
        unique=True,
        help_text='Обязательное поле. Только латиница.'
    )

    REQUIRED_FIELDS = ['name', 'slug']

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория произведения'
        verbose_name_plural = 'Категории произведений'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для информации о произведениях."""

    name = models.TextField(verbose_name='Название произведения')
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        db_index=True,
        validators=[
            MaxValueValidator(datetime.now().year)
        ],
        help_text='Год произведения не может превышать текущий.'
    )
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre, verbose_name='Название жанра',
        through='GenresTitle', related_name='genre_titles')
    category = models.ForeignKey(
        Category, verbose_name='Название категории',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='category_titles'
    )

    class Meta:
        verbose_name = 'Категория произведения'
        verbose_name_plural = 'Категории произведений'

    def __str__(self):
        return self.name


class GenresTitle(models.Model):
    """Модель для связи произведения и жанра."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Модель для ревью произведения."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title_reviews',
        verbose_name='Ревью к произведению',
        help_text='Ревью к произведению'
    )
    text = models.TextField(
        verbose_name='Текст ревью к произведению',
        help_text='Введите текст ревью.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_reviews',
        verbose_name='Ревью автора',
        help_text='Ревью с автором'
    )
    score = models. PositiveIntegerField(
        verbose_name='Оценка произведению',
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        help_text='Введите значение от 1 до 10'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Ревью пользователя'
        verbose_name_plural = 'Ревью пользователей'

        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author'],
                name='unuque_review',
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Модель для комментов под ревью."""

    review = models.ForeignKey(
        Review,
        blank=True,
        on_delete=models.CASCADE,
        related_name='review_comments',
        verbose_name='Комментарии под ревью',
        help_text='Комментариии под ревью'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_comments',
        verbose_name='Комментарии автора',
        help_text='Комментарии автора поста'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
