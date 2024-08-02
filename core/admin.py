from django.contrib import admin
from .models import Book, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publish_date", "created_at")
    list_filter = ("author", "publish_date")
    search_fields = ("title", "author", "description")
    date_hierarchy = "publish_date"
    inlines = [ReviewInline]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("book__title", "user__username", "review_text")
    date_hierarchy = "created_at"


admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
