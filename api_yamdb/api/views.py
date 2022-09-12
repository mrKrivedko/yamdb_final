from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Avg

from rest_framework import (
    viewsets,
    filters,
    mixins
)

from django_filters import rest_framework as dfilters

from reviews.models import (
    Category,
    Genre,
    Title,
    Review
)
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    CreateTitleSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer,
)
from api.permissions import (
    OnlyAdminOrReadonly,
    IsAuthorOrVIPRole
)
from api.filters import TitleGenreFilter


class ProjectBaseViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [OnlyAdminOrReadonly]


class CategoryViewSet(ProjectBaseViewSet):
    """Вьюсет для категории и жанров."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = ('slug')
    filter_backends = (dfilters.DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)


class GenreViewSet(ProjectBaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = ('slug')
    filter_backends = (dfilters.DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Title.objects.prefetch_related(
        'genre', 'category'
    ).annotate(rating=Avg('title_reviews__score'))
    permission_classes = [OnlyAdminOrReadonly]
    filter_backends = (dfilters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitleGenreFilter

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return TitleSerializer
        return CreateTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для ревью."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrVIPRole]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id).title_reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментов."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrVIPRole]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        # проверяем что ревью соответсвует указанному тайтлу
        get_list_or_404(
            get_object_or_404(Title, pk=title_id).title_reviews.all(),
            id=review_id
        )
        return get_object_or_404(Review, pk=review_id).review_comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
