from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from .filters import TitleFilter
from .models import Category, Genre, Title
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          TitleSerializerGet)


class MixinView(mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    pass


class GenreViewSet(MixinView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [IsAdminOrReadOnly, ]


class CategoryViewSet(MixinView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly, ]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly, ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerGet
        else:
            return TitleSerializer
