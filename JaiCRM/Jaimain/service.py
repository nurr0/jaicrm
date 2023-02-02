from datetime import datetime
import os
from typing import NoReturn

from .models import *
import JaiCRM.settings as settings
from Jaimain.resources import SalesResource


def sales_report(file_format: str, user_pk: int):  # , start: datetime.date, end: datetime.date
    user = JaiUser.objects.get(pk=user_pk)
    sales_resource = SalesResource(user=user)
    dataset = sales_resource.export()
    media_path = settings.MEDIA_ROOT + f'/reports/{user.partner.name}/'
    file_name_prefix = 'asdasd'

    if not os.path.exists(media_path):
        os.makedirs(media_path)

    if file_format == 'CSV':
        file_name = file_name_prefix + '.csv'
        file_path = media_path + file_name
        with open(file_path, 'wb') as f:
            f.write(dataset.csv.encode())
        ReportExport.objects.create(file=f'reports/{user.partner.name}/{file_name}',
                                    user=user,
                                    file_name=file_name)

    elif file_format == 'JSON':
        file_name = file_name_prefix + '.json'
        file_path = media_path + file_name
        with open(file_path, 'w') as f:
            f.write(dataset.json)
        ReportExport.objects.create(file=f'reports/{user.partner.name}/{file_name}',
                                    user=user,
                                    file_name=file_name)

    elif file_format == 'XLS (Excel)':
        file_name = file_name_prefix + '.xls'
        file_path = media_path + file_name
        with open(file_path, 'wb') as f:
            f.write(dataset.xls)
        ReportExport.objects.create(file=f'reports/{user.partner.name}/{file_name}',
                                    user=user,
                                    file_name=file_name)

