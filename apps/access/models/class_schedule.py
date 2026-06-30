from django.db import models
from django.core.exceptions import ValidationError


class ClassSchedule(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Segunda-feira"
        TUESDAY = 1, "Terca-feira"
        WEDNESDAY = 2, "Quarta-feira"
        THURSDAY = 3, "Quinta-feira"
        FRIDAY = 4, "Sexta-feira"
        SATURDAY = 5, "Sabado"
        SUNDAY = 6, "Domingo"

    teacher = models.ForeignKey(
        "access.Teacher",
        on_delete=models.PROTECT,
        related_name="class_schedules",
    )
    room = models.ForeignKey(
        "access.Room",
        on_delete=models.PROTECT,
        related_name="class_schedules",
    )
    subject = models.CharField(max_length=120)
    class_group = models.CharField(max_length=120)
    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices)
    starts_at = models.TimeField()
    ends_at = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("weekday", "starts_at", "subject")
        verbose_name = "horario de aula"
        verbose_name_plural = "horarios de aula"

    def __str__(self):
        return f"{self.subject} - {self.class_group}"

    def clean(self):
        super().clean()
        if self.starts_at and self.ends_at and self.ends_at <= self.starts_at:
            raise ValidationError({
                "ends_at": "O horario de termino deve ser posterior ao inicio.",
            })
