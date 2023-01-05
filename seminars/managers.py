from datetime import date
from portal.base._managers import BaseModelManager
from datetime import datetime

class SeminarManager(BaseModelManager):
    def get_active_seminar(self):
        return self.filter(start_date_time__gte = datetime.now())

class BookingManager(BaseModelManager):

    def get_active_booking(self):
        if self.alive_only:
            return self.filter(seminar__deleted_at=None).filter(deleted_at=None)
        else:
            return self.filter(seminar__deleted_at=None)

    def get_user_active_booking(self, user):
        if self.alive_only:
            return self.filter(seminar__deleted_at=None).filter(deleted_at=None, attendee=user)
        else:
            return self.filter(seminar__deleted_at=None).filter(attendee=user)

class RoomManager(BaseModelManager):
    None