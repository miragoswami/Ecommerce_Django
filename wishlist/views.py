from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Wishlist
from .serializers import WishlistSerializer


class WishlistViewSet(viewsets.ModelViewSet):

    serializer_class = WishlistSerializer   #"Use WishlistSerializer whenever you convert Wishlist data to/from JSON."
    permission_classes = [IsAuthenticated]   #Only authenticated users are allowed to use this ViewSet.

    def get_queryset(self):
        return Wishlist.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )