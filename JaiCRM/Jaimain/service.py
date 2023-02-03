from calendar import calendar, monthrange
from datetime import datetime
import os
from random import randint
from typing import NoReturn

from .models import *
import JaiCRM.settings as settings
from Jaimain.resources import SalesResource


def sales_report(file_format: str, user_pk: int):  # , start: datetime.date, end: datetime.date
    user = JaiUser.objects.get(pk=user_pk)
    sales_resource = SalesResource(user=user)
    dataset = sales_resource.export()
    media_path = settings.MEDIA_ROOT + f'/reports/{user.partner.name}/'
    file_name_prefix = f'Продажи {user} {datetime.now()}'

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


def data_for_sales_by_cat_donought(partner):
    sales = ProductInReceipt.objects.filter(receipt__partner=partner)\
        .values('product__product__category')\
        .annotate(sum_of_sales=Sum(F('price_with_discount') * F('amount')))\
        .order_by('product__product__category')
    cats = []
    sums = []
    for elem in sales:
        cats.append(ProductCategory.objects.get(pk=elem['product__product__category']).get_full_path())
        sums.append(int(elem['sum_of_sales']))
    data = [cats, sums]
    return data


def data_for_sales_by_shop_graph(partner):
    today = datetime.now()
    days_in_month = [i + 1 for i in range(today.day)]
    data = SellReceipt.objects.filter(partner=partner)

    result = {}
    for elem in data:
        shop = elem.shop.name
        day = elem.time_created.day
        sales = int(elem.get_total_price_with_discount())
        if shop in result:
            result[shop][day-1] += sales
        else:
            result[shop] = [0 for i in days_in_month]
            result[shop][day-1] = sales

    datasets = []
    for elem in result:
        datasets.append({'label': elem,
                         'data': result[elem],
                         'borderColor': f'rgb({randint(1,255)},{randint(1,255)},{randint(1,255)})',
                         'backgroundColor': f'rgb({randint(1,255)},{randint(1,255)},{randint(1,255)})'})

    return days_in_month, datasets

