from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.access.models import AccessEvent, Room
from apps.access.views.helpers import paginate, staff_required


@login_required
@staff_required
def event_list(request):
    events = AccessEvent.objects.select_related("room")
    room_id = request.GET.get("room")
    accepted = request.GET.get("accepted")
    event_type = request.GET.get("event_type")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    if room_id:
        events = events.filter(room_id=room_id)
    if accepted in ("true", "false"):
        events = events.filter(accepted=accepted == "true")
    if event_type:
        events = events.filter(event_type=event_type)
    if date_from:
        events = events.filter(occurred_at__date__gte=date_from)
    if date_to:
        events = events.filter(occurred_at__date__lte=date_to)

    page_obj = paginate(request, events)
    return render(
        request,
        "access/event_list.html",
        {
            "events": page_obj.object_list,
            "rooms": Room.objects.all(),
            "page_obj": page_obj,
        },
    )
