from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    product_image = serializers.ImageField(
        source="product.image",
        read_only=True
    )

    class Meta:
        model = OrderItem

        fields = [
            "id",
            "order",
            "product",
            "product_name",
            "product_image",
            "quantity",
            "price",
        ]

        read_only_fields = [
            "id",
            "order",
            "product_name",
            "product_image",
        ]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Order

        fields = [
            "id",
            "user",
            "total_price",
            "status",
            "created_at",
            "items",
        ]

        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]

    def create(self, validated_data):

        items_data = validated_data.pop(
            "items",
            []
        )

        order = Order.objects.create(
            **validated_data
        )

        for item_data in items_data:

            OrderItem.objects.create(
                order=order,
                **item_data
            )

        return order
        
# SELLER ORDER ITEM
       

class SellerOrderItemSerializer(
    serializers.ModelSerializer
):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    product_image = serializers.ImageField(
        source="product.image",
        read_only=True
    )

    class Meta:
        model = OrderItem

        fields = [
            "id",
            "product",
            "product_name",
            "product_image",
            "quantity",
            "price",
        ]

        read_only_fields = [
            "id",
            "product",
            "product_name",
            "product_image",
            "quantity",
            "price",
        ]


       
# SELLER ORDER
       

class SellerOrderSerializer(
    serializers.ModelSerializer
):

    customer_name = serializers.CharField(
        source="user.username",
        read_only=True
    )

    items = serializers.SerializerMethodField()

    seller_total = serializers.SerializerMethodField()

    class Meta:
        model = Order

        fields = [
            "id",
            "customer_name",
            "seller_total",
            "status",
            "created_at",
            "items",
        ]

        read_only_fields = [
            "id",
            "customer_name",
            "seller_total",
            "status",
            "created_at",
            "items",
        ]

    def get_items(self, order):

        seller = self.context[
            "request"
        ].user

        items = order.items.filter(
            product__seller=seller
        )

        serializer = SellerOrderItemSerializer(
            items,
            many=True,
            context=self.context
        )

        return serializer.data

    def get_seller_total(self, order):

        seller = self.context[
            "request"
        ].user

        items = order.items.filter(
            product__seller=seller
        )

        total = sum(
            item.price * item.quantity
            for item in items
        )

        return total