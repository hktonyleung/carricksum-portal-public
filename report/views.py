from .models import Report, ReportType
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import generic
from portal.base._mixin import SuperUserMixin, LoginRequiredMixin
from datetime import datetime
from pytz import UTC
from .tasks import gen_report
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from celery.result import AsyncResult
from django.utils.decorators import method_decorator
from account.decorators import otp2_required_with_title

from django.views.generic import View
from portal.utils import render_pdf_file
from portal.models import User
import time

# Create your views here.
class ReportListView(LoginRequiredMixin, generic.ListView):
    
    name = 'Report'
    context_object_name = 'reports'   # your own name for the list as a template variable
    template_name = 'report/index.html'  # Specify your own template name/location
    #paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        reports = Report.objects.get_user_active_report(user)
        #for seminar in seminars:
        if reports.count() == 0:
            #create empty report for user.
            all_report_type = ReportType.objects.all()
            for report_type in all_report_type:
                Report.objects.create(
                    name=report_type.name,
                    status='RE',
                    created_by=user,
                    type=report_type)

            reports = Report.objects.get_user_active_report(user)
        return reports

    @method_decorator(otp2_required_with_title(name))
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)


def report_generation(request, report_id):
    user_id = request.user.id
    task = gen_report.delay(user_id, report_id)
    time.sleep(0.5)
    return HttpResponseRedirect(reverse("report:report-index"))

class DownloadPdf(View):
    def get(self, request, *args, **kwargs):
        report_id = kwargs['report_id']
        user_id = request.user.id
        report = Report.objects.get(pk=report_id, created_by=User.objects.get(pk=user_id))
        raw_file = report.raw_file
        return HttpResponse(raw_file, content_type='application/pdf')

def check_task_status(request, task_id):
    status = AsyncResult(task_id).status
    response_data = {}
    response_data['status'] = status
    return JsonResponse(response_data)