
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    USER_TYPES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default='buyer'
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username





class SellerProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seller_profile"
    )

    business_name = models.CharField(
        max_length=150
    )

    store_name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.store_name