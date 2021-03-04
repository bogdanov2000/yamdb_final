import random

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .models import Category, Genre, Review, Title, User
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrStaff
from .serializers import (
    CategorySerializer,
    CheckCodeSerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SendCodeSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    UserSerializer,
)


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    A viewset that provides default `create()`, `destroy()`
    and `list()` actions.
    """

    pass


@api_view(["POST"])
def send_confirmation_code(request):
    serializer = SendCodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    email = request.data.get("email")
    confirmation_code = str(random.randint(10000, 99999))
    user = User.objects.filter(email=email).exists()
    if not user:
        User.objects.create_user(email=email)
    User.objects.filter(email=email).update(
        confirmation_code=make_password(
            confirmation_code, salt=None, hasher="default")
    )
    mail_subject = "Yamdb confirmation code"
    message = f"Your confirmation code: {confirmation_code}"
    send_mail(mail_subject, message, "Yamdb <no-reply@yamdb.com>", [email])
    return Response(f"The code was sent to {email}", status=status.HTTP_200_OK)


@api_view(["POST"])
def get_jwt_token(request):
    serializer = CheckCodeSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.data["email"]
    confirmation_code = serializer.data.get("confirmation_code")
    user = get_object_or_404(User, email=email)

    if confirmation_code != user.confirmation_code:
        return Response({"Bad confirmation code"},
         status=status.HTTP_400_BAD_REQUEST)

    token = AccessToken.for_user(user)
    return Response({"token": f"{token}"}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    serializer_class = UserSerializer
    lookup_field = "username"
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__username"]

    @action(
        methods=["patch", "get"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path="me",
        url_name="me",
    )
    def me(self, request, *args, **kwargs):
        if self.request.method == "PATCH":
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = self.get_serializer(request.user)

        return Response(serializer.data)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Title.objects.all().annotate(Avg("reviews__score"))
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleReadSerializer

        return TitleWriteSerializer


class GenreViewSet(ListCreateDestroyViewSet):
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["=name"]


class CategoryViewSet(ListCreateDestroyViewSet):
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["=name"]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrStaff)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrStaff)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()
