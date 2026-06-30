from django.db import models
from django.utils import timezone


class AccessEvent(models.Model):
    class Source(models.TextChoices):
        RFID = "rfid", "RFID"
        SYSTEM = "system", "Sistema"

    class EventType(models.TextChoices):
        RFID_OPEN_ATTEMPT = "rfid_open_attempt", "Tentativa de abertura RFID"
        RFID_CLOSE_ATTEMPT = "rfid_close_attempt", "Tentativa de fechamento RFID"

    source = models.CharField(max_length=20, choices=Source.choices)
    event_type = models.CharField(max_length=40, choices=EventType.choices)
    room = models.ForeignKey(
        "access.Room",
        on_delete=models.SET_NULL,
        related_name="access_events",
        blank=True,
        null=True,
    )
    identifier = models.CharField(max_length=120, blank=True)
    occurred_at = models.DateTimeField(default=timezone.now)
    accepted = models.BooleanField(default=False)
    denial_reason = models.CharField(max_length=255, blank=True)
    raw_payload = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ("-occurred_at", "-id")
        verbose_name = "evento de acesso"
        verbose_name_plural = "eventos de acesso"

    def __str__(self):
        status = "aceito" if self.accepted else "negado"
        return f"{self.get_event_type_display()} - {status}"
