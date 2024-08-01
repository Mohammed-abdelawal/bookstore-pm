from rest_framework import generics
from .serializers import RegisterSerializer, BookSerializer, ReviewSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .models import Book, Review


UserModel = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
