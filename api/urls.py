from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    get_jwt_token,
    send_confirmation_code,
)

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("titles", TitleViewSet, basename="titles")
router.register("genres", GenreViewSet, basename="genres")
router.register("categories", CategoryViewSet, basename="categories")

router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register(r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews")
router.register("users", UserViewSet)

urlpatterns = [
    path("v1/auth/email/", send_confirmation_code, name="get_token"),
    path("v1/auth/token/", get_jwt_token),
    path("v1/", include(router.urls)),
]
