from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, BookSerializer, ReviewSerializer
from .models import Book
from drf_yasg.utils import swagger_auto_schema

UserModel = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    Register a new user.
    """

    queryset = UserModel.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve a list of books or a specific book.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a review to a book.",
        request_body=ReviewSerializer,
        responses={
            status.HTTP_201_CREATED: ReviewSerializer,
            status.HTTP_400_BAD_REQUEST: "Validation Error",
        },
    )
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def add_review(self, request, pk=None):
        """
        Add a review to a specific book.
        """
        book = self.get_object()
        data = request.data
        data["book"] = book.id
        data["user"] = request.user.id
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user, book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
