from django.db import models
from django.db.models import Q
from django.utils import timezone


class RfidCard(models.Model):
    teacher = models.ForeignKey(
        "access.Teacher",
        on_delete=models.PROTECT,
        related_name="rfid_cards",
    )
    rfid_hash = models.CharField(max_length=64)
    rfid_suffix = models.CharField(max_length=8, blank=True)
    is_active = models.BooleanField(default=True)
    issued_at = models.DateTimeField(default=timezone.now)
    revoked_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("teacher__user__first_name", "teacher__user__last_name", "-issued_at")
        constraints = [
            models.UniqueConstraint(
                fields=("rfid_hash",),
                condition=Q(is_active=True, revoked_at__isnull=True),
                name="unique_active_rfid_hash",
            ),
        ]
        verbose_name = "cartao RFID"
        verbose_name_plural = "cartoes RFID"

    def __str__(self):
        return f"{self.teacher} - {self.masked_identifier}"

    @property
    def masked_identifier(self):
        if not self.rfid_suffix:
            return "****"
        return f"****{self.rfid_suffix}"
