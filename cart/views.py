from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(
            user=self.request.user
        )

    def get_cart(self):
        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )

        return cart

    @action(
        detail=False,
        methods=["post"]
    )
    def add(self, request):

        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        if not product_id:
            return Response(
                {"error": "Product ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity < 1:
            return Response(
                {"error": "Quantity must be at least 1"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = self.get_cart()

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={
                "quantity": quantity
            }
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartSerializer(cart)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=["patch"],
        url_path="update-quantity"
    )
    def update_quantity(self, request):

        item_id = request.data.get("item_id")
        quantity = int(request.data.get("quantity", 1))

        if not item_id:
            return Response(
                {"error": "Item ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity < 1:
            return Response(
                {"error": "Quantity must be at least 1"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = self.get_cart()

        try:
            item = CartItem.objects.get(
                id=item_id,
                cart=cart
            )
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        item.quantity = quantity
        item.save()

        serializer = CartSerializer(cart)

        return Response(serializer.data)

    @action(
        detail=False,
        methods=["delete"],
        url_path="remove"
    )
    def remove(self, request):

        item_id = request.data.get("item_id")

        if not item_id:
            return Response(
                {"error": "Item ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = self.get_cart()

        try:
            item = CartItem.objects.get(
                id=item_id,
                cart=cart
            )
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        item.delete()

        serializer = CartSerializer(cart)

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):

        cart = self.get_cart()

        serializer = CartSerializer(cart)

        return Response(serializer.data)