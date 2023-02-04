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

    # текущий месяц
    today = datetime.today()
    current_month = today.month
    current_day = today.day
    current_year = today.year
    sales_month = ProductInReceipt.objects.filter(receipt__partner=partner,
                                                  receipt__time_created__month=current_month,
                                                  receipt__time_created__year=current_year,
                                                  receipt__is_returned=False) \
        .values('product__product__category') \
        .annotate(sum_of_sales=Sum(F('price_with_discount') * F('amount'))) \
        .order_by('product__product__category')
    cats_month = []
    sums_month = []
    for elem in sales_month:
        cats_month.append(ProductCategory.objects.get(pk=elem['product__product__category']).get_full_path())
        sums_month.append(int(elem['sum_of_sales']))
    data_month = [cats_month, sums_month]

    # текущий день
    sales_day = ProductInReceipt.objects.filter(receipt__partner=partner,
                                                receipt__time_created__day=current_day,
                                                receipt__time_created__month=current_month,
                                                receipt__time_created__year=current_year,
                                                receipt__is_returned=False) \
        .values('product__product__category') \
        .annotate(sum_of_sales=Sum(F('price_with_discount') * F('amount'))) \
        .order_by('product__product__category')
    cats_day = []
    sums_day = []
    for elem in sales_day:
        cats_day.append(ProductCategory.objects.get(pk=elem['product__product__category']).get_full_path())
        sums_day.append(int(elem['sum_of_sales']))
    data_day = [cats_day, sums_day]

    # текущий год
    current_year = today.year
    sales_year = ProductInReceipt.objects.filter(receipt__partner=partner,
                                                 receipt__time_created__year=current_year,
                                                 receipt__is_returned=False) \
        .values('product__product__category') \
        .annotate(sum_of_sales=Sum(F('price_with_discount') * F('amount'))) \
        .order_by('product__product__category')
    cats_year = []
    sums_year = []
    for elem in sales_year:
        cats_year.append(ProductCategory.objects.get(pk=elem['product__product__category']).get_full_path())
        sums_year.append(int(elem['sum_of_sales']))
    data_year = [cats_year, sums_year]

    return data_day, data_month, data_year


def data_for_sales_by_shop_graph(partner):
    today = datetime.now()
    days_in_month = [i + 1 for i in range(today.day)]
    data = SellReceipt.objects.filter(partner=partner, is_returned=False)

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



def data_for_sales_by_payment_form_donought(partner):

    # текущий месяц
    today = datetime.today()
    current_month = today.month
    current_year = today.year
    current_day = today.day
    sales_month = ProductInReceipt.objects.filter(receipt__partner=partner,
                                                  receipt__time_created__month=current_month,
                                                  receipt__time_created__year=current_year,
                                                  receipt__is_returned=False) \
        .values('receipt__payment_form') \
        .annotate(sum_of_sales=Sum(F('price_with_discount') * F('amount'))) \
        .order_by('receipt__payment_form')
    payment_forms_month = []
    sums_month = []
    for elem in sales_month:
        payment_forms_month.append(PaymentForm.objects.get(pk=elem['receipt__payment_form']).name)
        sums_month.append(int(elem['sum_of_sales']))
    data_month = [payment_forms_month, sums_month]

    # текущий день
    sales_day = ProductInReceipt.objects.filter(receipt__partner=partner,
                                                receipt__time_created__day=current_day,
                                                receipt__time_created__month=current_month,
                                                receipt__time_created__year=current_year,
                                                receipt__is_returned=False) \
        .values('receipt__payment_form') \
        .annotate(sum_of_sales=Sum(F('price_with_discount') * F('amount'))) \
        .order_by('receipt__payment_form')
    payment_forms_day = []
    sums_day = []
    for elem in sales_day:
        payment_forms_day.append(PaymentForm.objects.get(pk=elem['receipt__payment_form']).name)
        sums_day.append(int(elem['sum_of_sales']))
    data_day = [payment_forms_day, sums_day]

    # текущий год
    sales_year = ProductInReceipt.objects.filter(receipt__partner=partner,
                                                 receipt__time_created__year=current_year,
                                                 receipt__is_returned=False) \
        .values('receipt__payment_form') \
        .annotate(sum_of_sales=Sum(F('price_with_discount') * F('amount'))) \
        .order_by('receipt__payment_form')
    payment_forms_year = []
    sums_year = []
    for elem in sales_year:
        payment_forms_year.append(PaymentForm.objects.get(pk=elem['receipt__payment_form']).name)
        sums_year.append(int(elem['sum_of_sales']))
    data_year = [payment_forms_year, sums_year]

    return data_day, data_month, data_year


def data_for_sales_by_sales_channel_donought(partner):

    # текущий месяц
    today = datetime.today()
    current_month = today.month
    current_year = today.year
    current_day = today.day
    sales_month = ProductInReceipt.objects.filter(receipt__partner=partner,
                                                  receipt__time_created__month=current_month,
                                                  receipt__time_created__year=current_year,
                                                  receipt__is_returned=False) \
        .values('receipt__sales_channel') \
        .annotate(sum_of_sales=Sum(F('price_with_discount') * F('amount'))) \
        .order_by('receipt__sales_channel')
    sales_channels_month = []
    sums_month = []
    for elem in sales_month:
        sales_channels_month.append(SalesChannel.objects.get(pk=elem['receipt__sales_channel']).name)
        sums_month.append(int(elem['sum_of_sales']))
    data_month = [sales_channels_month, sums_month]

    # текущий день
    sales_day = ProductInReceipt.objects.filter(receipt__partner=partner,
                                                receipt__time_created__day=current_day,
                                                receipt__time_created__month=current_month,
                                                receipt__time_created__year=current_year,
                                                receipt__is_returned=False) \
        .values('receipt__sales_channel') \
        .annotate(sum_of_sales=Sum(F('price_with_discount') * F('amount'))) \
        .order_by('receipt__sales_channel')
    sales_channels_day = []
    sums_day = []
    for elem in sales_day:
        sales_channels_day.append(SalesChannel.objects.get(pk=elem['receipt__sales_channel']).name)
        sums_day.append(int(elem['sum_of_sales']))
    data_day = [sales_channels_day, sums_day]

    # текущий год
    sales_year = ProductInReceipt.objects.filter(receipt__partner=partner,
                                                 receipt__time_created__year=current_year,
                                                 receipt__is_returned=False) \
        .values('receipt__sales_channel') \
        .annotate(sum_of_sales=Sum(F('price_with_discount') * F('amount'))) \
        .order_by('receipt__sales_channel')
    sales_channels_year = []
    sums_year = []
    for elem in sales_year:
        sales_channels_year.append(SalesChannel.objects.get(pk=elem['receipt__sales_channel']).name)
        sums_year.append(int(elem['sum_of_sales']))
    data_year = [sales_channels_year, sums_year]

    return data_day, data_month, data_year
