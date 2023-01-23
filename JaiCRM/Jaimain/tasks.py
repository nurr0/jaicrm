from .service import sales_report
from JaiCRM.celery import app


@app.task
def export_sales_report(file_format, user):
    sales_report(file_format, user)
