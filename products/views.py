from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # --------------------------------
    # PERMISSIONS
    # --------------------------------

    def get_permissions(self):

        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
            "my_products",
        ]:
            return [IsAuthenticated()]

        return [AllowAny()]

    # --------------------------------
    # QUERYSET
    # --------------------------------

    def get_queryset(self):  #Before allowing a request, decide what permission is required.

        if self.action == "my_products":

            return Product.objects.filter(
                seller=self.request.user
            )

        return Product.objects.all()

    # --------------------------------
    # CREATE
    # --------------------------------

    def perform_create(self, serializer):

        if self.request.user.user_type != "seller":

            raise PermissionDenied(
                "Only sellers can create products."
            )

        serializer.save(
            seller=self.request.user
        )

    # --------------------------------
    # UPDATE
    # --------------------------------

    def perform_update(self, serializer):

        product = self.get_object()

        if product.seller != self.request.user:

            raise PermissionDenied(
                "You can only edit your own products."
            )

        serializer.save()

    # --------------------------------
    # DELETE
    # --------------------------------

    def perform_destroy(self, instance):

        if instance.seller != self.request.user:

            raise PermissionDenied(
                "You can only delete your own products."
            )

        instance.delete()

    # --------------------------------
    # MY PRODUCTS
    # --------------------------------

    @action(
        detail=False,
        methods=["get"],
        url_path="my-products"
    )
    def my_products(self, request):

        products = self.get_queryset()

        serializer = self.get_serializer(
            products,
            many=True
        )

        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer