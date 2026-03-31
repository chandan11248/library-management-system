from django.urls import path
from . import views

# URL Routing - demonstrates Django URL patterns and named routes
urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Book CRUD operations
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/add/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),

    # Category
    path('categories/add/', views.category_create, name='category_create'),

    # Borrow / Return
    path('books/<int:pk>/borrow/', views.borrow_book, name='borrow_book'),
    path('borrow/<int:pk>/return/', views.return_book, name='return_book'),
    path('my-books/', views.my_books, name='my_books'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # API
    path('api/books/', views.api_books, name='api_books'),

    # Activity log
    path('activity-log/', views.activity_log, name='activity_log'),
]
