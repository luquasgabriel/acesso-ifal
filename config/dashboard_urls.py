from django.urls import path

from apps.access import views as access_views


urlpatterns = [
    path("", access_views.home, name="home"),
    path("historico/", access_views.history, name="history"),
    path("salas/", access_views.room_list, name="rooms"),
    path("salas/status/", access_views.room_status, name="room_status"),
    path("professores/", access_views.teacher_list, name="teachers"),
    path("horarios/", access_views.schedule_list, name="schedules"),
    path("acesso/rfid/", access_views.rfid_list, name="rfid_cards"),
    path("acesso/eventos/", access_views.event_list, name="access_events"),
]
