from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class APIUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email, username=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(email=email,
                          is_staff=True,
                          is_superuser=True,
                          **kwargs)
        user.set_password(password)
        user.save()
        return user


class UserRole(models.TextChoices):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(AbstractUser):

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    email = models.EmailField(("email"), blank=False, unique=True)
    bio = models.TextField(max_length=200, blank=True)
    confirmation_code = models.CharField(max_length=6, default="000000")
    role = models.CharField(
        max_length=30, choices=UserRole.choices, default=UserRole.USER
    )

    objects = APIUserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ("-id",)


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ("-id",)


class Genre(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ("-id",)


class Title(models.Model):
    name = models.CharField(max_length=90)
    year = models.IntegerField()
    description = models.TextField(max_length=200, blank=True)
    genre = models.ManyToManyField(Genre, related_name="titles")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="titles", null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-id",)


class Review(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name="reviews")
    text = models.CharField(max_length=400)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1),
                                MaxValueValidator(10)])
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ("-id",)


class Comment(models.Model):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name="comments")
    text = models.TextField()
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="comments")
    pub_date = models.DateTimeField("Дата публикации",
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ("-id",)