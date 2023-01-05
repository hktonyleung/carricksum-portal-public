from .models import Report, ReportType
from datetime import datetime

class RetrieveReport:
    def __init__(self):
        pass

    # Retrieve Inventory Reort
    def retrieve_invr(self, user):
        data = {
                'today': datetime.now(), 
                'amount': 40.99,
                'customer_name': user.username,
                'inventory_id': 1233434444,
        }
        return data

    # Retrieve Inventory Reort
    def retrieve_salr(self, user):
        data = {
                'today': datetime.now(), 
                'amount': 120.00,
                'customer_name': user.username,
                'sales_id': 2244,
        }
        return data

def retrieve_data(user, report: str):
    retrieve_report = RetrieveReport()
    method_name = f"retrieve_{report.lower()}"
    method_to_call = getattr(retrieve_report, method_name)

    return method_to_call(user)
