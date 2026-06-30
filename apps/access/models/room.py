from django.db import models


class Room(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Livre"
        IN_USE = "in_use", "Em uso"
        LOCKED = "locked", "Bloqueada"
        MAINTENANCE = "maintenance", "Manutencao"

    name = models.CharField(max_length=120)
    code = models.CharField(max_length=30, unique=True)
    location = models.CharField(max_length=120, blank=True)
    capacity = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )

    class Meta:
        ordering = ("name", "code")
        verbose_name = "sala"
        verbose_name_plural = "salas"

    def __str__(self):
        return f"{self.name} ({self.code})"
