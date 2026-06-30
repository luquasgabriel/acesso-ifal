import hashlib
import re
from datetime import datetime, timedelta

from django.db import transaction
from django.utils import timezone

from apps.access.models import AccessEvent, AccessSession, ClassSchedule, RfidCard, Room


DEFAULT_EARLY_OPEN_MINUTES = 15
DEFAULT_LATE_OPEN_MINUTES = 15


def normalize_rfid_uid(raw_uid):
    return re.sub(r"[^0-9A-Fa-f]", "", raw_uid or "").upper()


def hash_rfid_uid(raw_uid):
    normalized = normalize_rfid_uid(raw_uid)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def mask_rfid_uid(raw_uid):
    normalized = normalize_rfid_uid(raw_uid)
    return normalized[-4:]


def _event_identifier(raw_uid):
    suffix = mask_rfid_uid(raw_uid)
    return f"****{suffix}" if suffix else ""


def _create_event(event_type, room, raw_uid, accepted=False, denial_reason="", raw_payload=None, occurred_at=None):
    return AccessEvent.objects.create(
        source=AccessEvent.Source.RFID,
        event_type=event_type,
        room=room,
        identifier=_event_identifier(raw_uid),
        occurred_at=occurred_at or timezone.now(),
        accepted=accepted,
        denial_reason=denial_reason,
        raw_payload=raw_payload or {},
    )


def _combine_today(time_value, reference):
    local_reference = timezone.localtime(reference)
    return timezone.make_aware(
        datetime.combine(local_reference.date(), time_value),
        timezone.get_current_timezone(),
    )


def _find_active_card(raw_uid):
    normalized = normalize_rfid_uid(raw_uid)
    if not normalized:
        return None

    return RfidCard.objects.filter(
        rfid_hash=hash_rfid_uid(normalized),
        is_active=True,
        revoked_at__isnull=True,
        teacher__is_active=True,
    ).select_related("teacher", "teacher__user").first()


def _find_current_schedule(teacher, room, reference_time):
    weekday = reference_time.weekday()
    schedules = ClassSchedule.objects.filter(
        teacher=teacher,
        room=room,
        weekday=weekday,
        is_active=True,
    )

    for schedule in schedules:
        starts_at = _combine_today(schedule.starts_at, reference_time)
        ends_at = _combine_today(schedule.ends_at, reference_time)
        earliest = starts_at - timedelta(minutes=DEFAULT_EARLY_OPEN_MINUTES)
        latest = starts_at + timedelta(minutes=DEFAULT_LATE_OPEN_MINUTES)
        if earliest <= reference_time <= latest and reference_time <= ends_at:
            return schedule

    return None


@transaction.atomic
def process_rfid_event(raw_uid, room_code, raw_payload=None, occurred_at=None):
    occurred_at = occurred_at or timezone.now()
    room = Room.objects.select_for_update().filter(code=room_code).first()

    if not normalize_rfid_uid(raw_uid):
        return _create_event(
            AccessEvent.EventType.RFID_OPEN_ATTEMPT,
            room,
            raw_uid,
            denial_reason="UID RFID nao informado ou invalido.",
            raw_payload=raw_payload,
            occurred_at=occurred_at,
        ), None

    if not room:
        return _create_event(
            AccessEvent.EventType.RFID_OPEN_ATTEMPT,
            None,
            raw_uid,
            denial_reason="Sala nao encontrada.",
            raw_payload=raw_payload,
            occurred_at=occurred_at,
        ), None

    open_session = AccessSession.objects.filter(
        room=room,
        status=AccessSession.Status.OPEN,
    ).select_for_update().select_related("teacher", "room", "schedule").first()

    if open_session:
        return close_room_by_rfid(raw_uid, room, open_session, raw_payload, occurred_at)

    return open_room_by_rfid(raw_uid, room, raw_payload, occurred_at)


@transaction.atomic
def open_room_by_rfid(raw_uid, room, raw_payload=None, occurred_at=None):
    occurred_at = occurred_at or timezone.now()
    card = _find_active_card(raw_uid)

    if not card:
        event = _create_event(
            AccessEvent.EventType.RFID_OPEN_ATTEMPT,
            room,
            raw_uid,
            denial_reason="Cartao RFID desconhecido ou inativo.",
            raw_payload=raw_payload,
            occurred_at=occurred_at,
        )
        return event, None

    if room.status == Room.Status.IN_USE:
        event = _create_event(
            AccessEvent.EventType.RFID_OPEN_ATTEMPT,
            room,
            raw_uid,
            denial_reason="Sala ja esta marcada como em uso.",
            raw_payload=raw_payload,
            occurred_at=occurred_at,
        )
        return event, None

    if room.status in (Room.Status.LOCKED, Room.Status.MAINTENANCE):
        event = _create_event(
            AccessEvent.EventType.RFID_OPEN_ATTEMPT,
            room,
            raw_uid,
            denial_reason="Sala bloqueada ou em manutencao.",
            raw_payload=raw_payload,
            occurred_at=occurred_at,
        )
        return event, None

    teacher = card.teacher
    schedule = _find_current_schedule(teacher, room, occurred_at)
    if not schedule:
        event = _create_event(
            AccessEvent.EventType.RFID_OPEN_ATTEMPT,
            room,
            raw_uid,
            denial_reason="Professor sem aula prevista para esta sala e horario.",
            raw_payload=raw_payload,
            occurred_at=occurred_at,
        )
        return event, None

    existing_session = AccessSession.objects.filter(
        room=room,
        status=AccessSession.Status.OPEN,
    ).exists()
    if existing_session:
        event = _create_event(
            AccessEvent.EventType.RFID_OPEN_ATTEMPT,
            room,
            raw_uid,
            denial_reason="Sala ja possui sessao aberta.",
            raw_payload=raw_payload,
            occurred_at=occurred_at,
        )
        return event, None

    event = _create_event(
        AccessEvent.EventType.RFID_OPEN_ATTEMPT,
        room,
        raw_uid,
        accepted=True,
        raw_payload=raw_payload,
        occurred_at=occurred_at,
    )
    session = AccessSession.objects.create(
        schedule=schedule,
        teacher=teacher,
        room=room,
        opened_at=occurred_at,
        opened_by_event=event,
    )
    room.status = Room.Status.IN_USE
    room.save(update_fields=("status",))
    return event, session


@transaction.atomic
def close_room_by_rfid(raw_uid, room, session, raw_payload=None, occurred_at=None):
    occurred_at = occurred_at or timezone.now()
    card = _find_active_card(raw_uid)

    if not card:
        event = _create_event(
            AccessEvent.EventType.RFID_CLOSE_ATTEMPT,
            room,
            raw_uid,
            denial_reason="Cartao RFID desconhecido ou inativo.",
            raw_payload=raw_payload,
            occurred_at=occurred_at,
        )
        return event, session

    if session.status != AccessSession.Status.OPEN:
        event = _create_event(
            AccessEvent.EventType.RFID_CLOSE_ATTEMPT,
            room,
            raw_uid,
            denial_reason="Sessao ja esta encerrada.",
            raw_payload=raw_payload,
            occurred_at=occurred_at,
        )
        return event, session

    if card.teacher_id != session.teacher_id:
        event = _create_event(
            AccessEvent.EventType.RFID_CLOSE_ATTEMPT,
            room,
            raw_uid,
            denial_reason="Professor diferente do responsavel pela sessao.",
            raw_payload=raw_payload,
            occurred_at=occurred_at,
        )
        return event, session

    event = _create_event(
        AccessEvent.EventType.RFID_CLOSE_ATTEMPT,
        room,
        raw_uid,
        accepted=True,
        raw_payload=raw_payload,
        occurred_at=occurred_at,
    )
    session.closed_at = occurred_at
    session.status = AccessSession.Status.CLOSED
    session.closed_by_event = event
    session.save(update_fields=("closed_at", "status", "closed_by_event"))

    room.status = Room.Status.AVAILABLE
    room.save(update_fields=("status",))
    return event, session
