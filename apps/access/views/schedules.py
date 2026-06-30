from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.access.models import ClassSchedule, Room, Teacher


@login_required
def schedule_list(request):
    schedules = ClassSchedule.objects.select_related("teacher__user", "room")
    if request.user.is_staff:
        pass
    elif hasattr(request.user, "teacher_profile"):
        schedules = schedules.filter(teacher=request.user.teacher_profile)
    else:
        schedules = schedules.none()

    teacher_id = request.GET.get("teacher")
    room_id = request.GET.get("room")
    weekday = request.GET.get("weekday")

    if teacher_id and request.user.is_staff:
        schedules = schedules.filter(teacher_id=teacher_id)
    if room_id:
        schedules = schedules.filter(room_id=room_id)
    if weekday != "" and weekday is not None:
        schedules = schedules.filter(weekday=weekday)

    return render(
        request,
        "schedules/list.html",
        {
            "schedules": schedules,
            "teachers": Teacher.objects.select_related("user").filter(is_active=True),
            "rooms": Room.objects.all(),
        },
    )
