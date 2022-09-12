from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    Review,
    Comment,
    Category,
    Genre,
    Title
)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = tuple(Category.REQUIRED_FIELDS)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = tuple(Genre.REQUIRED_FIELDS)


class CreateTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для создания тайтла."""

    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Title


class GenresTitleSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор для поля genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведения."""

    genre = GenresTitleSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title
        read_only_fields = ('id',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'score',
            'author',
            'title',
            'pub_date'
        )
        read_only_fields = ('id', 'title')

    def validate_score(self, value):
        """Валидация оценки."""

        if value not in [i for i in range(1, 11)]:
            raise serializers.ValidationError(
                'Оценка не в диапазоне от 1 до 10'
            )
        return value

    def validate(self, data):
        """Автор может оставлять только один review на title."""

        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if self.context.get('request').method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError('Отзыв уже существует!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
