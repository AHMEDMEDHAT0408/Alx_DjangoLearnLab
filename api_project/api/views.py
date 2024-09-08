from rest_framework import viewsets
from .models import Book
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access this

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]  # Only admins can modify data
        return super().get_permissions()

