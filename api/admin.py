from django.contrib import admin

# Register your models here.

from .models import Comment, Review, Title, Genre, Category, User

admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(User)
