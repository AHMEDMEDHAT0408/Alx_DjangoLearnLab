from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate  # Importing login, logout, and authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.http import HttpResponse
from .models import Book  # Assuming Book model is in the same app

# Task 1: Implementing User Authentication in Django
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to a home page or any other view
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page or any other view
        else:
            return render(request, 'relationship_app/login.html', {'error': 'Invalid username or password'})
    return render(request, 'relationship_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

# Task 2: Implementing Role-Based Access Control in Django
def is_admin(user):
    return user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

def is_member(user):
    return user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# Task 3: Implementing Custom Permissions in Django
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        # code to add a book
        return redirect('book_list')  # Redirect after adding a book
    return render(request, 'relationship_app/add_book.html')

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    # Fetch the book by ID
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        # code to edit a book
        return redirect('book_detail', book_id=book.id)  # Redirect after editing a book
    return render(request, 'relationship_app/edit_book.html', {'book': book})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    # Fetch the book by ID
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        book.delete()  # code to delete a book
        return redirect('book_list')  # Redirect after deleting a book
    return render(request, 'relationship_app/delete_book.html', {'book': book})
