from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render

from apps.access.models import Teacher
from apps.access.views.helpers import staff_required


@login_required
@staff_required
def teacher_list(request):
    teachers = Teacher.objects.select_related("user").annotate(
        active_rfid_count=Count(
            "rfid_cards",
            filter=Q(rfid_cards__is_active=True, rfid_cards__revoked_at__isnull=True),
        )
    )
    search = request.GET.get("search")
    if search:
        teachers = teachers.filter(
            Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(user__email__icontains=search)
            | Q(employee_number__icontains=search)
        )
    return render(request, "people/teacher_list.html", {"teachers": teachers})
