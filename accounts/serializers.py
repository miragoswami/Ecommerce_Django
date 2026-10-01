from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


from .models import SellerProfile


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        email = attrs.get("email", "").strip()
        password = attrs.get("password")

        # Find user by email (case-insensitive)
        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            # Also allow logging in with username as email field
            user = User.objects.filter(username__iexact=email).first()

        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password"
            )

        # Check credentials
        authenticated_user = authenticate(
            username=user.username,
            password=password
        )

        if authenticated_user is None:
            raise serializers.ValidationError(
                "Invalid email or password"
            )

        if not authenticated_user.is_active:
            raise serializers.ValidationError(
                "User account is inactive"
            )

        # Create JWT tokens
        refresh = RefreshToken.for_user(authenticated_user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": authenticated_user.id,
                "username": authenticated_user.username,
                "email": authenticated_user.email,
                "user_type": authenticated_user.user_type,
            }
        }

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "password",
            "phone",
        ]

    def create(self, validated_data):

        # Get password separately
        password = validated_data.pop("password")

        # Create user
        user = User(**validated_data)

        # Encrypt/hash password
        user.set_password(password)

        # Save user in database
        user.save()

        return user



class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
        ]

        read_only_fields = [
            "id",
        ]

    def validate_email(self, value):

        user = self.instance

        if User.objects.exclude(
            id=user.id
        ).filter(
            email__iexact=value
        ).exists():

            raise serializers.ValidationError(
                "This email is already registered."
            )

        return value

    def validate_username(self, value):

        user = self.instance

        if User.objects.exclude(
            id=user.id
        ).filter(
            username__iexact=value
        ).exists():

            raise serializers.ValidationError(
                "This username is already taken."
            )

        return value





class SellerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerProfile

        fields = [
            "id",
            "business_name",
            "store_name",
            "phone",
            "address",
            "city",
            "state",
            "pincode",
            "description",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]