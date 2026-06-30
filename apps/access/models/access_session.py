from django.db import models
from django.db.models import Q
from django.utils import timezone


class AccessSession(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Aberta"
        CLOSED = "closed", "Fechada"
        CANCELLED = "cancelled", "Cancelada"

    schedule = models.ForeignKey(
        "access.ClassSchedule",
        on_delete=models.PROTECT,
        related_name="access_sessions",
    )
    teacher = models.ForeignKey(
        "access.Teacher",
        on_delete=models.PROTECT,
        related_name="access_sessions",
    )
    room = models.ForeignKey(
        "access.Room",
        on_delete=models.PROTECT,
        related_name="access_sessions",
    )
    opened_at = models.DateTimeField(default=timezone.now)
    closed_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )
    opened_by_event = models.ForeignKey(
        "access.AccessEvent",
        on_delete=models.SET_NULL,
        related_name="opened_sessions",
        blank=True,
        null=True,
    )
    closed_by_event = models.ForeignKey(
        "access.AccessEvent",
        on_delete=models.SET_NULL,
        related_name="closed_sessions",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("-opened_at", "-id")
        constraints = [
            models.UniqueConstraint(
                fields=("room",),
                condition=Q(status="open"),
                name="unique_open_access_session_per_room",
            ),
        ]
        verbose_name = "sessao de acesso"
        verbose_name_plural = "sessoes de acesso"

    def __str__(self):
        return f"{self.room} - {self.teacher} - {self.opened_at:%d/%m/%Y %H:%M}"

    @property
    def duration(self):
        if not self.closed_at:
            return None
        return self.closed_at - self.opened_at
