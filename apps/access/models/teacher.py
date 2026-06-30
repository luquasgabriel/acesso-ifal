from django.conf import settings
from django.db import models


class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
    )
    employee_number = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("user__first_name", "user__last_name", "employee_number")
        verbose_name = "professor"
        verbose_name_plural = "professores"

    def __str__(self):
        name = self.user.get_full_name()
        return name or self.user.username
