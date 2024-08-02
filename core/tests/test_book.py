from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.models import Book, Review
from django.utils import timezone

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
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(Review.objects.filter(book=self.book).count(), 2)
        self.assertEqual(Review.objects.get(review_text="Awesome book!").rating, 4)

    def test_duplicate_review(self):
        url = reverse("books-add-review", args=[self.book.id])
        data = {"review_text": "Duplicate review", "rating": 3}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), 1)  # Still only one review

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
