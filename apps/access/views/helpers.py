from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test


def is_admin_user(user):
    return user.is_authenticated and user.is_staff


staff_required = user_passes_test(is_admin_user)


def paginate(request, queryset, per_page=20):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get("page"))
