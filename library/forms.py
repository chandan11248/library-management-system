from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Category


class BookForm(forms.ModelForm):
    """Form for adding/editing books - demonstrates form data handling."""
    published_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'category', 'published_date',
                  'copies_available', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 13-digit ISBN'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'copies_available': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CategoryForm(forms.ModelForm):
    """Form for managing categories."""
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class UserRegistrationForm(UserCreationForm):
    """Custom registration form - demonstrates authentication concepts."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})


class SearchForm(forms.Form):
    """Search form - demonstrates GET request handling."""
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search books by title or author...',
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
