from django.db import models
from orders.models import Order


class Payment(models.Model):

    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )

    payment_method = models.CharField(
        max_length=50
    )

    transaction_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Payment {self.id}"