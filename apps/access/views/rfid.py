import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.access.models import RfidCard
from apps.access.services import process_rfid_event
from apps.access.views.helpers import staff_required


@login_required
@staff_required
def rfid_list(request):
    cards = RfidCard.objects.select_related("teacher__user")
    search = request.GET.get("search")
    status = request.GET.get("status")

    if search:
        cards = cards.filter(
            Q(teacher__user__first_name__icontains=search)
            | Q(teacher__user__last_name__icontains=search)
            | Q(teacher__employee_number__icontains=search)
            | Q(rfid_suffix__icontains=search)
        )
    if status == "active":
        cards = cards.filter(is_active=True, revoked_at__isnull=True)
    elif status == "revoked":
        cards = cards.filter(Q(is_active=False) | Q(revoked_at__isnull=False))

    return render(request, "access/rfid_list.html", {"cards": cards})


@csrf_exempt
@require_POST
def rfid_event(request):
    expected_token = getattr(settings, "RFID_API_TOKEN", "")
    if expected_token:
        auth_header = request.headers.get("Authorization", "")
        if auth_header != f"Bearer {expected_token}":
            return JsonResponse({"accepted": False, "error": "Token RFID invalido."}, status=401)

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"accepted": False, "error": "JSON invalido."}, status=400)

    raw_uid = payload.get("rfid_uid") or payload.get("uid") or payload.get("rfid_id")
    room_code = payload.get("room_code") or payload.get("device_id")
    occurred_at_value = payload.get("occurred_at") or payload.get("timestamp")
    occurred_at = parse_datetime(occurred_at_value) if occurred_at_value else None
    if occurred_at and timezone.is_naive(occurred_at):
        occurred_at = timezone.make_aware(occurred_at, timezone.get_current_timezone())

    if not raw_uid or not room_code:
        return JsonResponse(
            {"accepted": False, "error": "rfid_uid e room_code sao obrigatorios."},
            status=400,
        )

    event, session = process_rfid_event(raw_uid, room_code, raw_payload=payload, occurred_at=occurred_at)
    return JsonResponse(
        {
            "accepted": event.accepted,
            "event_id": event.id,
            "session_id": session.id if session else None,
            "denial_reason": event.denial_reason,
        },
        status=200 if event.accepted else 403,
    )
