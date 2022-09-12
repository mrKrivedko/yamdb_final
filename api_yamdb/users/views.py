from api.permissions import OnlyAdmin, OnlyAuthorOrVIPRole
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User
from users.serializers import CreateUserSerialiser, GetUserSerializer, SignupSerialiser, TokenCreateSerialiser


class SignupViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Вьюсет для регистрации."""

    serializer_class = SignupSerialiser
    queryset = User.objects.all()
    lookup_field = User._meta.pk.name

    def get_permissions(self):
        self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_instance(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )

    def perform_create(self, serializer):
        user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        user.email_user('Your confirmation_code: ', f'{confirmation_code}')
        user = serializer.save(confirmation_code=confirmation_code)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с users/."""

    serializer_class = CreateUserSerialiser
    queryset = User.objects.all()
    lookup_field = User.USERNAME_FIELD
    permission_classes = [OnlyAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('username',)

    def get_permissions(self):
        if self.action == "me":
            self.permission_classes = [OnlyAuthorOrVIPRole]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "username":
            return GetUserSerializer
        return super().get_serializer_class()

    def get_instance(self):
        return self.request.user

    def perform_update(self, serializer):
        if (
            self.request.user.role == 'user'
        ) and (
            not self.request.user.is_superuser
        ) and (
            self.request.data.get(
                'role'
            ) in ['moderator', 'admin']
        ):
            serializer.save(role='user')
        else:
            serializer.save()

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":

            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            # здесь тесты требуют чтобы на delete выбрасывал 405
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(['get', "post", "patch"], detail=False)
    def username(self, request, username=None, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)


class CreateTokenView(generics.CreateAPIView):
    """Вью для создания токена."""

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = TokenCreateSerialiser(data=request.data)
        if serializer.is_valid():
            confirmation_code = serializer.validated_data.get(
                'confirmation_code'
            )
            user = get_object_or_404(
                User, username=serializer.validated_data.get('username')
            )
            if user.confirmation_code == confirmation_code:
                token = RefreshToken.for_user(user).access_token
                return Response(
                    data={'token': str(token)}, status=status.HTTP_200_OK
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
