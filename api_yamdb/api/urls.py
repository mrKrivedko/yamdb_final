from django.urls import include, path

from rest_framework.routers import DefaultRouter

from users.views import SignupViewSet, UserViewSet, CreateTokenView

from api.views import (
    ReviewViewSet,
    CommentViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet
)

router = DefaultRouter()

router.register('auth/signup', SignupViewSet, basename='signup')
router.register('users', UserViewSet, basename='users')

router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('auth/token/', CreateTokenView.as_view()),
    path('', include(router.urls),),
]
