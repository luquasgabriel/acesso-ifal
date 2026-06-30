from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from apps.access.models import AccessSession, Room
from apps.access.views.helpers import staff_required


@login_required
@staff_required
def room_list(request):
    rooms = Room.objects.all()
    search = request.GET.get("search")
    status = request.GET.get("status")

    if search:
        rooms = rooms.filter(Q(name__icontains=search) | Q(code__icontains=search) | Q(location__icontains=search))
    if status:
        rooms = rooms.filter(status=status)

    return render(request, "rooms/list.html", {"rooms": rooms})


@login_required
def room_status(request):
    rooms = list(Room.objects.all())
    open_sessions = AccessSession.objects.filter(
        status=AccessSession.Status.OPEN,
    ).select_related("room", "teacher__user", "schedule")
    sessions_by_room = {session.room_id: session for session in open_sessions}
    for room in rooms:
        room.current_session = sessions_by_room.get(room.id)

    return render(
        request,
        "rooms/status.html",
        {
            "rooms": rooms,
        },
    )
