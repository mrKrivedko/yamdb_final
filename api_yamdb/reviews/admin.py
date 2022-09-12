from django.contrib import admin

from users.models import User
from reviews.models import (
    Review,
    Comment,
    Category,
    Title,
    Genre,
    GenresTitle
)


class ReviewAdmin(admin.ModelAdmin):
    """Админка для review."""
    list_display = (
        'pk',
        'title_id',
        'author',
        'score',
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    """Админка для comment."""
    list_display = (
        'pk',
        'review_id',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('text', 'author')
    empty_value_display = '-пусто-'


admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(GenresTitle)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
