
from django.urls import path
from report.views import ReportListView, DownloadPdf, report_generation, check_task_status

app_name = 'report'

urlpatterns = [    
    path("index", ReportListView.as_view(), name="report-index"),
    path("generate/<str:report_id>", report_generation, name="report-generate"),
    #path("generate/<str:report_id>", run_task, name="report-generate"),
    path("check_task_status/<str:task_id>", check_task_status, name="check-task-status"),
    #path("render_pdf", GeneratePdf.as_view(), name="render-pdf"),
    path("download/<str:report_id>", DownloadPdf.as_view(), name="report-download"),
]