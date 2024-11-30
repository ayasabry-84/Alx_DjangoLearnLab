from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Book
from django.contrib.auth.models import User


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

        # Create some test data
        self.book1 = Book.objects.create(title="Book 1", author="Author 1", published_date="2021-01-01")
        self.book2 = Book.objects.create(title="Book 2", author="Author 2", published_date="2022-01-01")

        # URLs
        self.list_url = reverse('book-list')  # Update with the actual name of the list view URL
        self.detail_url = lambda pk: reverse('book-detail', kwargs={"pk": pk})  # Update with detail view URL


def test_get_books(self):
    response = self.client.get(self.list_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 2)

def test_create_book(self):
    data = {"title": "Book 3", "author": "Author 3", "published_date": "2023-01-01"}
    response = self.client.post(self.list_url, data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Book.objects.count(), 3)
    self.assertEqual(Book.objects.last().title, "Book 3")

def test_update_book(self):
    data = {"title": "Updated Book 1"}
    response = self.client.put(self.detail_url(self.book1.id), data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.book1.refresh_from_db()
    self.assertEqual(self.book1.title, "Updated Book 1")

def test_delete_book(self):
    response = self.client.delete(self.detail_url(self.book1.id))
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Book.objects.count(), 1)

def test_filter_books_by_title(self):
    response = self.client.get(self.list_url, {"title": "Book 1"})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]["title"], "Book 1")

def test_search_books(self):
    response = self.client.get(self.list_url, {"search": "Author 2"})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]["author"], "Author 2")

def test_order_books_by_published_date(self):
    response = self.client.get(self.list_url, {"ordering": "published_date"})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data[0]["title"], "Book 1")  # Oldest first

def test_permissions_for_unauthenticated_users(self):
    self.client.logout()
    response = self.client.post(self.list_url, {"title": "Book 3"})
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

