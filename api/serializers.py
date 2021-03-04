from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Category, Comment, Genre, Review, Title, User


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class CheckCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("first_name",
                  "last_name",
                  "username",
                  "bio",
                  "email",
                  "role")
        model = User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        lookup_field = "slug"
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        lookup_field = "slug"
        model = Category


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(source="reviews__score__avg",
                                      read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = ("id",
                  "name",
                  "year",
                  "rating",
                  "description",
                  "genre",
                  "category")
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        fields = ("id", "name", "year", "description", "genre", "category")
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = (
            "id",
            "review",
            "text",
            "author",
            "pub_date",
        )
        model = Comment
        read_only_fields = (
            "review",
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    def validate(self, data):
        if self.context["request"].method == "POST":
            user = self.context["request"].user
            title_id = self.context["request"]
            .parser_context["kwargs"]["title_id"]
            if Review.objects.filter(author=user, title__id=title_id).exists():
                raise serializers.ValidationError(
                    "Вы уже оставили отзыв на данное произведение"
                )

        return super().validate(data)

    class Meta:
        fields = ("id", "title", "text", "author", "score", "pub_date")
        model = Review
        read_only_fields = (
            "title",
        )
