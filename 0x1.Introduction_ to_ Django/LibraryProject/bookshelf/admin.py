from django.contrib import admin
from .models import Book

# Define a custom admin interface for the Book model
class BookAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add search functionality to search by title and author
    search_fields = ('title', 'author')
    
    # Add filters to filter by publication year
    list_filter = ('publication_year',)

# Register the Book model with the custom admin interface
admin.site.register(Book, BookAdmin)
