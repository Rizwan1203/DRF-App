from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Item


class ItemAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.item_data = {
            "name": "Test Item",
            "description": "Test Description",
            "created_by": self.user.id,
        }

    def test_create_item(self):
        url = reverse("item-list-create")
        response = self.client.post(url, self.item_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, "Test Item")
        self.assertEqual(Item.objects.get().created_by, self.user)

    def test_list_items(self):
        # Create an item
        Item.objects.create(
            name="Test Item", description="Test Description", created_by=self.user
        )

        url = reverse("item-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Item")
        self.assertEqual(response.data[0]["created_by"], self.user.id)

    def test_retrieve_update_destroy_item(self):
        # Create an item
        item = Item.objects.create(
            name="Test Item", description="Test Description", created_by=self.user
        )

        url = reverse("item-retrieve-update-destroy", args=[item.id])

        # Retrieve
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Item")
        self.assertEqual(response.data["created_by"], self.user.id)

        # Update
        updated_data = {
            "name": "Updated Item",
            "description": "Updated Description",
            "created_by": self.user.id,
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.get(id=item.id).name, "Updated Item")

        # Patch
        patch_data = {"name": "Patched Name"}
        response = self.client.patch(url, patch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.get(id=item.id).name, "Patched Name")

        # Destroy
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

    def test_create_item_with_invalid_data(self):
        url = reverse("item-list-create")
        invalid_data = {"name": "", "description": "Invalid Description"}
        response = self.client.post(url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_nonexistent_item(self):
        url = reverse(
            "item-retrieve-update-destroy", args=[999]
        )  # Assuming 999 is an invalid item ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_item(self):
        url = reverse(
            "item-retrieve-update-destroy", args=[999]
        )  # Assuming 999 is an invalid item ID
        response = self.client.put(
            url,
            {"name": "Updated Item", "description": "Updated Description"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_nonexistent_item(self):
        url = reverse(
            "item-retrieve-update-destroy", args=[999]
        )  # Assuming 999 is an invalid item ID
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
