"""
Management command to seed the database with sample data.
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from library.models import Category, Book
from datetime import date


class Command(BaseCommand):
    help = 'Seeds the database with sample library data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create categories
        categories_data = [
            ('Fiction', 'Novels, short stories, and literary fiction'),
            ('Science', 'Physics, chemistry, biology, and general science'),
            ('Technology', 'Computer science, programming, and IT'),
            ('History', 'World history, civilizations, and historical events'),
            ('Mathematics', 'Algebra, calculus, statistics, and pure mathematics'),
        ]

        categories = {}
        for name, desc in categories_data:
            cat, created = Category.objects.get_or_create(name=name, defaults={'description': desc})
            categories[name] = cat
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  Category: {name} [{status}]')

        # Create books
        books_data = [
            ('To Kill a Mockingbird', 'Harper Lee', '9780061120084', 'Fiction', '1960-07-11', 3),
            ('1984', 'George Orwell', '9780451524935', 'Fiction', '1949-06-08', 5),
            ('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 'Fiction', '1925-04-10', 2),
            ('A Brief History of Time', 'Stephen Hawking', '9780553380163', 'Science', '1988-04-01', 4),
            ('The Selfish Gene', 'Richard Dawkins', '9780199291151', 'Science', '1976-01-01', 2),
            ('Clean Code', 'Robert C. Martin', '9780132350884', 'Technology', '2008-08-01', 6),
            ('Design Patterns', 'Gang of Four', '9780201633610', 'Technology', '1994-10-31', 3),
            ('Python Crash Course', 'Eric Matthes', '9781593279288', 'Technology', '2019-05-03', 4),
            ('Sapiens', 'Yuval Noah Harari', '9780062316097', 'History', '2011-01-01', 5),
            ('Guns, Germs, and Steel', 'Jared Diamond', '9780393317558', 'History', '1997-03-01', 2),
            ('Calculus Made Easy', 'Silvanus Thompson', '9780312185480', 'Mathematics', '1910-01-01', 3),
            ('Introduction to Algorithms', 'Thomas Cormen', '9780262033848', 'Technology', '2009-07-31', 4),
        ]

        for title, author, isbn, cat_name, pub_date, copies in books_data:
            book, created = Book.objects.get_or_create(
                isbn=isbn,
                defaults={
                    'title': title,
                    'author': author,
                    'category': categories[cat_name],
                    'published_date': date.fromisoformat(pub_date),
                    'copies_available': copies,
                    'description': f'A classic work in {cat_name.lower()} literature.',
                }
            )
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  Book: {title} [{status}]')

        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@library.com', 'admin123')
            self.stdout.write('  Superuser: admin / admin123 [Created]')
        else:
            self.stdout.write('  Superuser: admin [Exists]')

        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
