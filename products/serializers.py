from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    seller_name = serializers.CharField(
        source="seller.username",
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "image",
            "created_at",
            "updated_at",
            "seller",
            "seller_name",
            "category",
            "category_name",
        ]
        read_only_fields = [
    "seller",
    "seller_name",
    "category_name",
    "created_at",
    "updated_at",
]