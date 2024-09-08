# API Views for Book Model

## ListView (Retrieve all books)
- URL: `/api/books/`
- HTTP Method: `GET`
- Permissions: Public (Unauthenticated users can view)

## DetailView (Retrieve a single book)
- URL: `/api/books/<int:pk>/`
- HTTP Method: `GET`
- Permissions: Public

## CreateView (Add a new book)
- URL: `/api/books/create/`
- HTTP Method: `POST`
- Permissions: Authenticated users only

## UpdateView (Modify an existing book)
- URL: `/api/books/<int:pk>/update/`
- HTTP Method: `PUT`, `PATCH`
- Permissions: Authenticated users only

## DeleteView (Remove a book)
- URL: `/api/books/<int:pk>/delete/`
- HTTP Method: `DELETE`
- Permissions: Authenticated users only
