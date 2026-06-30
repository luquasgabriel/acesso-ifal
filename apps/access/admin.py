from django import forms
from django.contrib import admin
from django.utils import timezone

from apps.access.models import (
    AccessEvent,
    AccessSession,
    ClassSchedule,
    RfidCard,
    Room,
    Teacher,
)
from apps.access.services.rfid import hash_rfid_uid, mask_rfid_uid


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("user", "employee_number", "is_active")
    list_filter = ("is_active",)
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "employee_number",
    )


class RfidCardAdminForm(forms.ModelForm):
    rfid_uid = forms.CharField(
        label="UID RFID",
        required=False,
        help_text="Informe o UID bruto. O sistema armazena apenas hash e sufixo.",
    )

    class Meta:
        model = RfidCard
        fields = ("teacher", "rfid_uid", "is_active", "issued_at", "revoked_at")

    def clean(self):
        cleaned_data = super().clean()
        rfid_uid = cleaned_data.get("rfid_uid")
        is_active = cleaned_data.get("is_active")
        if not self.instance.pk and not rfid_uid:
            self.add_error("rfid_uid", "Informe o UID RFID.")
        if rfid_uid and is_active:
            duplicate = RfidCard.objects.filter(
                rfid_hash=hash_rfid_uid(rfid_uid),
                is_active=True,
                revoked_at__isnull=True,
            )
            if self.instance.pk:
                duplicate = duplicate.exclude(pk=self.instance.pk)
            if duplicate.exists():
                self.add_error("rfid_uid", "Ja existe um cartao RFID ativo com este UID.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        rfid_uid = self.cleaned_data.get("rfid_uid")
        if rfid_uid:
            instance.rfid_hash = hash_rfid_uid(rfid_uid)
            instance.rfid_suffix = mask_rfid_uid(rfid_uid)
        if not instance.is_active and not instance.revoked_at:
            instance.revoked_at = timezone.now()
        if commit:
            instance.save()
            self.save_m2m()
        return instance


@admin.register(RfidCard)
class RfidCardAdmin(admin.ModelAdmin):
    form = RfidCardAdminForm
    list_display = ("teacher", "masked_identifier", "is_active", "issued_at", "revoked_at")
    list_filter = ("is_active", "issued_at", "revoked_at")
    readonly_fields = ("rfid_hash", "rfid_suffix")
    search_fields = (
        "teacher__user__username",
        "teacher__user__email",
        "teacher__employee_number",
        "rfid_suffix",
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "location", "capacity", "status")
    list_filter = ("status",)
    search_fields = ("name", "code", "location")


@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ("subject", "class_group", "teacher", "room", "weekday", "starts_at", "ends_at", "is_active")
    list_filter = ("weekday", "is_active", "room")
    search_fields = (
        "subject",
        "class_group",
        "teacher__user__first_name",
        "teacher__user__last_name",
        "room__name",
        "room__code",
    )


@admin.register(AccessSession)
class AccessSessionAdmin(admin.ModelAdmin):
    list_display = ("room", "teacher", "schedule", "opened_at", "closed_at", "status")
    list_filter = ("status", "room", "opened_at")
    search_fields = (
        "room__name",
        "room__code",
        "teacher__user__first_name",
        "teacher__user__last_name",
        "schedule__subject",
    )
    readonly_fields = ("opened_by_event", "closed_by_event")


@admin.register(AccessEvent)
class AccessEventAdmin(admin.ModelAdmin):
    list_display = ("occurred_at", "source", "event_type", "room", "accepted", "denial_reason")
    list_filter = ("source", "event_type", "accepted", "occurred_at")
    search_fields = ("identifier", "room__name", "room__code", "denial_reason")
    readonly_fields = (
        "source",
        "event_type",
        "room",
        "identifier",
        "occurred_at",
        "accepted",
        "denial_reason",
        "raw_payload",
    )
