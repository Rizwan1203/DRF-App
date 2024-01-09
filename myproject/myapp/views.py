from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Item
from .serializers import ItemListCreateSerializer, ItemSerializer


@extend_schema(tags=["item"])
class ItemListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemListCreateSerializer

    def get_queryset(self):
        return Item.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@extend_schema(tags=["item"])
class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.filter(created_by=self.request.user)
