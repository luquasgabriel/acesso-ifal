from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.access.models import AccessSession, ClassSchedule, Room, Teacher
from apps.access.views.helpers import paginate


WEEK_CALENDAR_DAYS = (
    (ClassSchedule.Weekday.MONDAY, "Seg"),
    (ClassSchedule.Weekday.TUESDAY, "Ter"),
    (ClassSchedule.Weekday.WEDNESDAY, "Qua"),
    (ClassSchedule.Weekday.THURSDAY, "Qui"),
    (ClassSchedule.Weekday.FRIDAY, "Sex"),
    (ClassSchedule.Weekday.SATURDAY, "Sáb"),
)


def _visible_schedules_for_user(user, teacher):
    schedules = ClassSchedule.objects.filter(is_active=True).select_related(
        "room",
        "teacher__user",
    ).order_by(
        "weekday",
        "starts_at",
        "ends_at",
        "subject",
        "room__name",
    )

    if user.is_staff:
        return schedules
    if teacher:
        return schedules.filter(teacher=teacher)
    return schedules.none()


def _build_week_calendar_rows(schedules):
    weekdays = [weekday for weekday, _label in WEEK_CALENDAR_DAYS]
    rows_by_time = {}

    for schedule in schedules:
        if schedule.weekday not in weekdays:
            continue

        key = (schedule.starts_at, schedule.ends_at)
        row = rows_by_time.setdefault(
            key,
            {
                "starts_at": schedule.starts_at,
                "ends_at": schedule.ends_at,
                "schedules_by_weekday": {weekday: [] for weekday in weekdays},
            },
        )
        row["schedules_by_weekday"][schedule.weekday].append(schedule)

    rows = []
    for key in sorted(rows_by_time):
        row = rows_by_time[key]
        rows.append(
            {
                "starts_at": row["starts_at"],
                "ends_at": row["ends_at"],
                "days": [
                    {
                        "weekday": weekday,
                        "label": label,
                        "schedules": row["schedules_by_weekday"][weekday],
                    }
                    for weekday, label in WEEK_CALENDAR_DAYS
                ],
            }
        )

    return rows


@login_required
def home(request):
    teacher = Teacher.objects.filter(user=request.user, is_active=True).first()
    schedules = list(_visible_schedules_for_user(request.user, teacher))

    sessions = AccessSession.objects.select_related("room", "teacher__user", "schedule")
    if request.user.is_staff:
        pass
    elif teacher:
        sessions = sessions.filter(teacher=teacher)
    else:
        sessions = sessions.none()

    context = {
        "calendar_colspan": len(WEEK_CALENDAR_DAYS) + 1,
        "calendar_rows": _build_week_calendar_rows(schedules),
        "calendar_weekdays": [
            {"weekday": weekday, "label": label}
            for weekday, label in WEEK_CALENDAR_DAYS
        ],
        "stats": {
            "rooms": Room.objects.count(),
            "rooms_in_use": Room.objects.filter(status=Room.Status.IN_USE).count(),
            "open_sessions": sessions.filter(status=AccessSession.Status.OPEN).count(),
            "teachers": Teacher.objects.filter(is_active=True).count(),
        },
        "recent_sessions": sessions[:5],
    }
    return render(request, "dashboard/home.html", context)


@login_required
def history(request):
    sessions = AccessSession.objects.select_related("room", "teacher__user", "schedule")
    teacher = Teacher.objects.filter(user=request.user, is_active=True).first()
    if request.user.is_staff:
        pass
    elif teacher:
        sessions = sessions.filter(teacher=teacher)
    else:
        sessions = sessions.none()

    room_id = request.GET.get("room")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    if room_id:
        sessions = sessions.filter(room_id=room_id)
    if date_from:
        sessions = sessions.filter(opened_at__date__gte=date_from)
    if date_to:
        sessions = sessions.filter(opened_at__date__lte=date_to)

    page_obj = paginate(request, sessions)
    return render(
        request,
        "dashboard/history.html",
        {
            "sessions": page_obj.object_list,
            "rooms": Room.objects.all(),
            "page_obj": page_obj,
        },
    )
