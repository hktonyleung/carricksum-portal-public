from portal.base._managers import BaseModelManager

class BranchManager(BaseModelManager):
    def get_active_branches(self):
        #return self.filter(active = True)
        return self.filter(deleted_at=None)

