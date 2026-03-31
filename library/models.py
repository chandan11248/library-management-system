from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Category model for classifying books - demonstrates relational DB concepts."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """Book model - demonstrates ORM concepts with ForeignKey relationships."""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='books'
    )
    published_date = models.DateField()
    copies_available = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def is_available(self):
        return self.copies_available > 0


class BorrowRecord(models.Model):
    """Tracks book borrowing - demonstrates Many-to-Many through model."""
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrow_records')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_records')
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed')

    class Meta:
        ordering = ['-borrow_date']

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"


class ActivityLog(models.Model):
    """Stores activity logs from middleware - demonstrates logging middleware."""
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=500)
    user = models.CharField(max_length=150, default='Anonymous')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    status_code = models.IntegerField(null=True, blank=True)
    response_time_ms = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.timestamp}] {self.method} {self.path} - {self.user}"
