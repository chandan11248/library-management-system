from django.contrib import admin
from .models import Book, Category, BorrowRecord, ActivityLog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'copies_available', 'created_at')
    list_filter = ('category', 'published_date')
    search_fields = ('title', 'author', 'isbn')


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'return_date', 'status')
    list_filter = ('status',)


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'method', 'path', 'user', 'status_code', 'response_time_ms')
    list_filter = ('method', 'status_code')
    readonly_fields = ('timestamp', 'method', 'path', 'user', 'ip_address', 'status_code', 'response_time_ms')
