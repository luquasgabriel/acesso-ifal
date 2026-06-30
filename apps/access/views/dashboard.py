from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.access.models import AccessSession, ClassSchedule, Room, Teacher
from apps.access.views.helpers import paginate


@login_required
def home(request):
    teacher = Teacher.objects.filter(user=request.user, is_active=True).first()
    schedules = ClassSchedule.objects.none()
    if teacher:
        schedules = ClassSchedule.objects.filter(
            teacher=teacher,
            is_active=True,
        ).select_related("room", "teacher__user")[:6]

    sessions = AccessSession.objects.select_related("room", "teacher__user", "schedule")
    if request.user.is_staff:
        pass
    elif teacher:
        sessions = sessions.filter(teacher=teacher)
    else:
        sessions = sessions.none()

    context = {
        "classes": schedules,
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
