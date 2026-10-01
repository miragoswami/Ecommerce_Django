from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    SellerProfileSerializer,
)





class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    # GET PROFILE
    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        })

    # UPDATE PROFILE
    def patch(self, request):
        user = request.user

        user.username = request.data.get(
            "username",
            user.username
        )

        user.email = request.data.get(
            "email",
            user.email
        )

        user.save()

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        })


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    # GET PROFILE
    def get(self, request):

        serializer = ProfileSerializer(
            request.user
        )

        return Response(
            serializer.data
        )

    # UPDATE PROFILE
    def patch(self, request):

        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )




class BecomeSellerView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Check whether user is already a seller

        if request.user.user_type == "seller":
            return Response(
                {
                    "message": "You are already a seller."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SellerProfileSerializer(
            data=request.data
        )

        if serializer.is_valid():

            seller_profile = serializer.save(
                user=request.user
            )

            # Change user from customer to seller

            request.user.user_type = "seller"
            request.user.save()

            return Response(
                {
                    "message": "Seller account created successfully.",
                    "seller_profile": SellerProfileSerializer(
                        seller_profile
                    ).data,
                    "user_type": request.user.user_type,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )