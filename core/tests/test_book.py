from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Book, Review
from django.utils import timezone
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


UserModel = get_user_model()


class BookStoreTests(APITestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.user2 = UserModel.objects.create_user(
            username="testuser2", password="testpassword2"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            description="Description",
            publish_date=timezone.now(),
        )
        self.review = Review.objects.create(
            user=self.user, book=self.book, review_text="Great book!", rating=5
        )
        self.access_token = self.get_access_token("testuser", "testpassword")
        self.access_token2 = self.get_access_token("testuser2", "testpassword2")

    def get_access_token(self, username, password):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"username": username, "password": password}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data["access"]

    def test_view_books_unauthenticated(self):
        url = reverse("books-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_view_books_authenticated(self):
        url = reverse("books-list")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Book")
        self.assertEqual(len(response.data[0]["reviews"]), 1)
        self.assertEqual(response.data[0]["reviews"][0]["review_text"], "Great book!")

    def test_view_book_detail_unauthenticated(self):
        url = reverse("books-detail", args=[self.book.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_view_book_detail_authenticated(self):
        url = reverse("books-detail", args=[self.book.id])
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Book")
        self.assertEqual(len(response.data["reviews"]), 1)
        self.assertEqual(response.data["reviews"][0]["review_text"], "Great book!")

    def test_add_review(self):
        url = reverse("books-add-review", args=[self.book.id])
        data = {"review_text": "Awesome book!", "rating": 4}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token2}")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(Review.objects.filter(book=self.book).count(), 2)
        self.assertEqual(Review.objects.get(review_text="Awesome book!").rating, 4)

    def test_duplicate_review(self):
        # First review is already created in setUp
        # now trying to create another one with the same user and book
        try:
            duplicate_review = Review.objects.create(
                user=self.user, book=self.book, review_text="Duplicate review", rating=3
            )
            duplicate_review.full_clean()
            duplicate_review.save()
        except IntegrityError as e:
            self.assertIn("unique constraint", str(e))
        else:
            self.fail("IntegrityError not raised for duplicate review")

    def test_review_rating_validation(self):
        url = reverse("books-add-review", args=[self.book.id])
        data = {
            "review_text": "Invalid rating",
            "rating": 6,  # Invalid rating, should fail
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token2}")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("rating", response.data)
        self.assertEqual(
            Review.objects.count(), 1
        )  # No new review added due to validation failure


class BookModelTests(TestCase):

    def test_upload_invalid_file_extension(self):
        invalid_file = SimpleUploadedFile(
            "test.txt", b"This is a test file.", content_type="text/plain"
        )
        book = Book(
            title="Test Book with Invalid File",
            author="Author",
            description="Description",
            publish_date=timezone.now(),
            file=invalid_file,
        )
        with self.assertRaises(ValidationError) as context:
            book.full_clean()  # This will trigger the validation
        self.assertIn("file", context.exception.message_dict)

    def test_upload_valid_file_extension(self):
        valid_file = SimpleUploadedFile(
            "test.pdf", b"%PDF-1.4 test file content", content_type="application/pdf"
        )
        book = Book(
            title="Test Book with Valid File",
            author="Author",
            description="Description",
            publish_date=timezone.now(),
            file=valid_file,
        )
        try:
            book.full_clean()  # This will trigger the validation
            book.save()
        except ValidationError:
            self.fail("Valid PDF file raised ValidationError unexpectedly!")

        self.assertEqual(Book.objects.count(), 1)
        self.assertTrue(
            Book.objects.get(title="Test Book with Valid File").file.name.endswith(
                ".pdf"
            )
        )

    def test_upload_file_size_limit(self):
        oversized_content = b"A" * int(
            settings.BOOK_FILE_SIZE_LIMIT_MB * 1024 * 1024 + 1
        )
        oversized_file = SimpleUploadedFile(
            "test.pdf", oversized_content, content_type="application/pdf"
        )
        book = Book(
            title="Test Book with Oversized File",
            author="Author",
            description="Description",
            publish_date=timezone.now(),
            file=oversized_file,
        )
        with self.assertRaises(ValidationError) as context:
            book.full_clean()  # This will trigger the validation
        self.assertIn("file", context.exception.message_dict)
