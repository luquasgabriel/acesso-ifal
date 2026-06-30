from .audit import event_list
from .dashboard import history, home
from .people import teacher_list
from .rfid import rfid_event, rfid_list
from .rooms import room_list, room_status
from .schedules import schedule_list

__all__ = [
    "event_list",
    "history",
    "home",
    "rfid_event",
    "rfid_list",
    "room_list",
    "room_status",
    "schedule_list",
    "teacher_list",
]
