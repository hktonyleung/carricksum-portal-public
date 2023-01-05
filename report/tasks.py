import random
from celery import shared_task
import time
from datetime import datetime
from .models import Report
from portal.models import User
from portal.utils import render_to_pdf_obj
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile
from .report import retrieve_data

@shared_task
def add(x, y):
    return x + y

@shared_task(name="report_generation")
def gen_report(user_id, report_id):
    
    user = User.objects.get(pk=user_id)
    report = Report.objects.get(pk=report_id, created_by=User.objects.get(pk=user_id))
    report.generate_start_date = datetime.now()
    report.status = "GE"
    report.save()
    

    # Retreive Report Data by report type
    data = retrieve_data(user, report.type.code)

    # Lookup Report Template from ReportType
    template = report.type.template_path

    time.sleep(1)
    
    # Include extra data if necessary
    data['test'] = 'test'

    result = render_to_pdf_obj(template, data)
    
    filename = "report.pdf"
    pdf_content = ContentFile(result.getvalue(), filename)

    report.raw_file.save(filename, pdf_content)
    report.generate_end_date = datetime.now()
    report.status = "CO"
    report.save()

    return True

@shared_task
def create_task(task_type, user, report_id):
    print("create task - start")
    time.sleep(int(task_type) * 10)
    print("create task - end")
    return True
