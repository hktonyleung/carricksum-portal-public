from portal.base._managers import BaseModelManager

class ReportManager(BaseModelManager):
    def get_user_active_report(self, user):
        if self.alive_only:
            return self.filter(deleted_at=None).filter(deleted_at=None, created_by=user)
        else:
            return self.filter(deleted_at=None).filter(create_by=user)


class ReportTypeManager(BaseModelManager):
    pass

