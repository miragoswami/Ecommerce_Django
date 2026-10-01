from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status

from .models import Order
from .serializers import (
    OrderSerializer,
    SellerOrderSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    # --------------------------------
    # GET ORDERS
    # --------------------------------

    def get_queryset(self):

        # Seller orders
        if self.action == "seller_orders":

            return Order.objects.filter(
                items__product__seller=self.request.user
            ).distinct()

        # Customer orders
        return Order.objects.filter(
            user=self.request.user
        )

    # --------------------------------
    # CREATE ORDER
    # --------------------------------

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )

    # --------------------------------
    # SELLER ORDERS
    # --------------------------------

    @action(
        detail=False,
        methods=["get"],
        url_path="seller-orders"
    )
    def seller_orders(self, request):

        if request.user.user_type != "seller":

            raise PermissionDenied(
                "Only sellers can view seller orders."
            )

        orders = self.get_queryset()

        serializer = SellerOrderSerializer(
            orders,
            many=True,
            context={
                "request": request
            }
        )

        return Response(
            serializer.data
        )

    # --------------------------------
    # SELLER UPDATE ORDER STATUS
    # --------------------------------

    @action(
        detail=True,
        methods=["patch"],
        url_path="seller-status"
    )
    def seller_status(self, request, pk=None):

        if request.user.user_type != "seller":

            raise PermissionDenied(
                "Only sellers can update order status."
            )

        order = Order.objects.filter(
            id=pk
        ).first()

        if order is None:

            return Response(
                {
                    "detail": "Order not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        seller_has_product = order.items.filter(
            product__seller=request.user
        ).exists()

        if not seller_has_product:

            raise PermissionDenied(
                "You can only update orders containing your products."
            )

        new_status = request.data.get("status")

        if not new_status:

            return Response(
                {
                    "status": "Status is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_statuses = dict(
            Order.STATUS_CHOICES
        ).keys()

        if new_status not in valid_statuses:

            return Response(
                {
                    "status": "Invalid order status."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        return Response(
            {
                "message": "Order status updated successfully.",
                "order_id": order.id,
                "status": order.status,
            },
            status=status.HTTP_200_OK
        )

    # --------------------------------
    # BUYER CANCEL ORDER
    # --------------------------------

    @action(
        detail=True,
        methods=["post"],
        url_path="cancel"
    )
    def cancel_order(self, request, pk=None):

        # get_queryset() already limits this
        # to the logged-in buyer's orders
        order = self.get_object()

        # Only pending or processing orders
        # can be canceled
        if order.status not in [
            "pending",
            "processing"
        ]:

            return Response(
                {
                    "detail":
                    "This order can no longer be canceled."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = "canceled"
        order.save()

        return Response(
            {
                "message":
                "Order canceled successfully.",
                "order_id": order.id,
                "status": order.status,
            },
            status=status.HTTP_200_OK
        )