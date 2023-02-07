from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F
from django.urls import reverse
from django.utils.safestring import mark_safe
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import Sum, Max


class Partner(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Наименование партнера')
    logo = models.ImageField(upload_to='logos/', verbose_name='Логотип')
    description = models.TextField(blank=True, verbose_name='Описание')
    iin = models.CharField(max_length=12, verbose_name="ИИН/БИН", unique=True, blank=False)
    partner_person = models.CharField(max_length=255, verbose_name='Контактное лицо')
    partner_tel = models.CharField(max_length=255, verbose_name='Контактный телефон')
    partner_email = models.EmailField(verbose_name='Контактный email')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_start_working = models.DateField(verbose_name='Дата начала работы')
    time_expires = models.DateField(verbose_name='Дата окончания работы')
    is_working = models.BooleanField(default=False, verbose_name='Активность')
    receipt_prefix = models.CharField(default=None, blank=True, null=True, verbose_name='Префикс чека', max_length=100)

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
        ordering = ['id']

    def __str__(self):
        return self.name


class JaiUser(AbstractUser):
    partner = models.ForeignKey('Partner', on_delete=models.PROTECT, verbose_name="Партнер", default=None, null=True)
    tel_number = models.CharField(max_length=255, verbose_name='Контактный телефон')

    def __str__(self):
        return self.username


class Shop(models.Model):
    partner = models.ForeignKey('Partner', on_delete=models.PROTECT, verbose_name="Партнер", null=False)
    name = models.CharField(max_length=255, unique=True, verbose_name='Наименование торговой точки')
    location = models.CharField(max_length=255, unique=True, verbose_name='Адрес')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_working = models.BooleanField(default=True, verbose_name='Активность')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    user = models.ForeignKey(JaiUser, verbose_name='Пользователь', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Торговая точка'
        verbose_name_plural = 'Торговые точки'
        ordering = ['id']

    def __str__(self):
        return self.name


class ProductCategory(MPTTModel):
    partner = models.ForeignKey('Partner', on_delete=models.PROTECT, verbose_name='Партнер', null=False)
    name = models.CharField(max_length=255, verbose_name='Наименование категории',
                            error_messages={
                                'unique_together': 'Категория с таким же названием и родительской категорией уже существует'})
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    description = models.TextField(blank=True, verbose_name='Описание', default=None, null=True)
    user = models.ForeignKey(JaiUser, verbose_name='Пользователь', on_delete=models.PROTECT)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('partner', 'name', 'parent'),)
        verbose_name = 'Товарная категория'
        verbose_name_plural = 'Товарные категории'

    def get_absolute_url(self):
        return reverse(f'category/{self.pk}')

    def __str__(self):
        return self.name

    def get_full_path(self):
        path = list(self.get_ancestors())
        path_str = '/'.join([node.name for node in path])
        path_str += f'/{self.name}'
        return path_str


class ProductProperty(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование свойства')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name='Партнер')
    user = models.ForeignKey(JaiUser, verbose_name='Пользователь', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('partner', 'name'),)
        verbose_name = 'Свойство товара'
        verbose_name_plural = 'Свойства товаров'


class SKU(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование', blank=False, null=False)
    image = models.ImageField(upload_to=f'product_images/', verbose_name='Изображение', blank=True, default=None,
                              null=True)
    description = models.TextField(blank=True, verbose_name='Описание', default=None, null=True)
    identifier = models.CharField(blank=False, max_length=255, null=False, verbose_name='Артикул', unique=True)
    producer = models.CharField(blank=False, max_length=255, null=False, verbose_name='Производитель')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name='Партнер')
    category = TreeForeignKey(ProductCategory, on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return f'{self.identifier} / {self.name}'

    def get_properties(self):
        properties = ProductPropertyRelation.objects.filter(product=self)
        properties_list = [f"{p.property.name} - {p.value}" for p in properties]
        # properties_string = '\n'.join(properties_list)
        return properties_list

    class Meta:
        unique_together = (('partner', 'identifier', 'name'),)
        verbose_name = 'SKU'
        verbose_name_plural = 'SKU'


class ProductPropertyRelation(models.Model):
    product = models.ForeignKey(SKU, on_delete=models.CASCADE, verbose_name='SKU')
    property = models.ForeignKey(ProductProperty, on_delete=models.CASCADE, verbose_name='Свойство')
    value = models.CharField(max_length=255, verbose_name='Значение')

    def __str__(self):
        return f'{self.product} - {self.property} - {self.value}'

    class Meta:
        unique_together = (('product', 'property'),)
        verbose_name = 'Связь свойства и товара'
        verbose_name_plural = 'Связи свойств и товаров'


class ProductInStock(models.Model):
    product = models.ForeignKey(SKU, on_delete=models.PROTECT, verbose_name='Товар')
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT, verbose_name='Торговая точка')
    amount = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return f'[{self.shop}] {self.product.__str__()}'

    def get_latest_supply_date(self):
        latest_supply = self.product.productsinsupply_set.filter(supply__warehouse=self.shop).latest(
            'supply__date_created').supply
        return latest_supply.date_created

    def get_latest_supply_price(self):
        latest_supply_cost = self.product.productsinsupply_set.filter(supply__warehouse=self.shop).latest(
            'supply__date_created').product_supply_price
        return latest_supply_cost

    def get_sell_price(self):
        sell_price = SellPrice.objects.get(product_in_stock=self).price
        return sell_price

    def get_retail_price_id(self):
        retail_price_id = SellPrice.objects.get(product_in_stock=self).pk
        return retail_price_id

    class Meta:
        unique_together = (('product', 'shop'),)


class Supply(models.Model):
    supplier = models.CharField(max_length=255, verbose_name='Поставщик')
    document = models.CharField(max_length=255, verbose_name='Документ')
    date = models.DateField(verbose_name='Дата')
    date_created = models.DateField(auto_now_add=True)
    warehouse = models.ForeignKey(Shop, verbose_name='Торговая точка', on_delete=models.PROTECT)
    partner = models.ForeignKey(Partner, on_delete=models.PROTECT, verbose_name='Партнер')

    class Meta:
        unique_together = (('supplier', 'document'),)

    def __str__(self):
        return self.document

    def get_total_amount_of_SKU(self):
        return ProductsInSupply.objects.filter(supply=self).values('product').distinct().count()

    def get_total_amount_of_products(self):
        return ProductsInSupply.objects.filter(supply=self).aggregate(Sum('amount'))['amount__sum']

    def get_total_cost_of_supply(self):
        total_cost = 0
        for unit in ProductsInSupply.objects.filter(supply=self):
            total_cost += unit.get_total_cost()
        return total_cost


class ProductsInSupply(models.Model):
    supply = models.ForeignKey(Supply, verbose_name='Поставка', on_delete=models.PROTECT)
    product = models.ForeignKey(SKU, verbose_name='Товар', on_delete=models.PROTECT)
    amount = models.IntegerField(verbose_name='Количество')
    product_supply_price = models.DecimalField(verbose_name='Закупочная стоимость', decimal_places=2, max_digits=11)

    def get_total_cost(self):
        return self.product_supply_price * self.amount

    def __str__(self):
        return self.product.__str__()

    class Meta:
        unique_together = (('product', 'supply'),)

class ProductsRemove(models.Model):
    shop = models.ForeignKey(Shop, verbose_name='Склад', on_delete=models.PROTECT)
    product = models.ForeignKey(ProductInStock, verbose_name='Товар', on_delete=models.PROTECT)
    decrease_amount = models.IntegerField(verbose_name='Количество')
    reason = models.CharField(max_length=255, verbose_name='Основание')
    date_created = models.DateField(auto_now_add=True)
    user_created = models.ForeignKey(JaiUser, on_delete=models.PROTECT)


class SellPrice(models.Model):
    product_in_stock = models.ForeignKey(ProductInStock, verbose_name='Товар', on_delete=models.PROTECT)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=11)
    partner = models.ForeignKey(Partner, verbose_name='Партнер', on_delete=models.PROTECT)

    class Meta:
        unique_together = (('product_in_stock', 'partner'),)


class SalesChannel(models.Model):
    name = models.CharField(max_length=254, verbose_name='Наименование канала продаж')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name='Партнер')
    user = models.ForeignKey(JaiUser, verbose_name='Пользователь', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('partner', 'name'),)
        verbose_name = 'Канал продаж'
        verbose_name_plural = 'Каналы продаж'


class PaymentForm(models.Model):
    name = models.CharField(max_length=254, verbose_name='Наименование канала продаж')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name='Партнер')
    user = models.ForeignKey(JaiUser, verbose_name='Пользователь', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('partner', 'name'),)
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'


class Customer(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.PROTECT, verbose_name='Партнер')
    firstname = models.CharField(max_length=255, verbose_name='Имя')
    lastname = models.CharField(max_length=255, verbose_name='Фамилия')
    tel_number = models.CharField(max_length=255, verbose_name='Номер телефона')
    gender = models.CharField(max_length=255, verbose_name='Пол')
    birthdate = models.DateField(verbose_name='Дата рождения')
    city = models.CharField(max_length=255, verbose_name='Город проживания')

    class Meta:
        unique_together = (('partner', 'firstname', 'lastname', 'birthdate'),)
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.lastname} {self.firstname} [{self.tel_number}]'

    def get_points_amount(self):
        points_achieved = Points.objects.filter(customer=self, receive_or_spend='recieve'). \
            values('points_amount'). \
            aggregate(Sum('points_amount'))['points_amount__sum']

        points_spend = Points.objects.filter(customer=self, receive_or_spend='spend'). \
            values('points_amount'). \
            aggregate(Sum('points_amount'))['points_amount__sum']
        if not points_achieved:
            points_achieved = 0
        if not points_spend:
            points_spend = 0
        points_amount = points_achieved - points_spend

        return points_amount


class SellReceipt(models.Model):
    partner = models.ForeignKey(Partner, verbose_name='Партнер', on_delete=models.PROTECT)
    user_created = models.ForeignKey(JaiUser, verbose_name='Пользователь', on_delete=models.PROTECT)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время регистрации чека')
    number = models.IntegerField(verbose_name='Номер чека')
    is_returned = models.BooleanField(verbose_name='Возврат', default=False)
    shop = models.ForeignKey(Shop, verbose_name='Торговая точка', on_delete=models.PROTECT)
    sales_channel = models.ForeignKey(SalesChannel, verbose_name='Канал продаж', on_delete=models.DO_NOTHING)
    payment_form = models.ForeignKey(PaymentForm, verbose_name='Способ оплаты', on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, verbose_name='Клиент', on_delete=models.DO_NOTHING, null=True, default=None,
                                 blank=True)

    class Meta:
        unique_together = (('partner', 'number'),)

    @staticmethod
    def get_receipt_number_for_partner(partner):
        last_number = SellReceipt.objects.filter(partner=partner).aggregate(Max('number'))['number__max']
        if last_number:
            return last_number + 1
        else:
            return 1

    def __str__(self):
        return f'{self.partner.receipt_prefix} {self.number}'

    def get_total_amount_of_SKU_in_receipt(self):
        return ProductInReceipt.objects.filter(receipt=self).values('product').distinct().count()

    def get_total_amount_of_products_in_receipt(self):
        return ProductInReceipt.objects.filter(receipt=self).aggregate(Sum('amount'))['amount__sum']

    def get_total_price(self):
        total_cost = 0
        for i in ProductInReceipt.objects.filter(receipt=self):
            total_cost += i.get_total_cost()
        return total_cost

    def get_total_discount(self):
        total_discount = 0
        for i in ProductInReceipt.objects.filter(receipt=self):
            total_discount += i.get_total_discount()
        return total_discount

    def get_total_price_with_discount(self):
        total_cost_with_discount = 0
        for i in ProductInReceipt.objects.filter(receipt=self):
            total_cost_with_discount += i.get_total_cost_with_discount()
        return total_cost_with_discount


class ProductInReceipt(models.Model):
    product = models.ForeignKey(ProductInStock, verbose_name='Товар', on_delete=models.PROTECT)
    amount = models.IntegerField(verbose_name='Количество')
    receipt = models.ForeignKey(SellReceipt, verbose_name='Чек', on_delete=models.PROTECT)
    price_in_stock = models.DecimalField(verbose_name='Установленная цена', decimal_places=2, max_digits=11)
    discount = models.IntegerField(verbose_name='Скидка', blank=True, default=0)
    price_with_discount = models.DecimalField(verbose_name='Цена с учетом скидки', decimal_places=2, max_digits=11)

    class Meta:
        unique_together = (('receipt', 'product'),)

    def get_total_cost(self):
        return self.amount * self.price_in_stock

    def get_total_discount(self):
        return self.amount * self.discount

    def get_total_cost_with_discount(self):
        return self.amount * self.price_with_discount


class ReportExport(models.Model):
    file = models.FileField(upload_to='reports/', verbose_name='Файл')
    user = models.ForeignKey(JaiUser, on_delete=models.PROTECT, verbose_name='Пользователь')
    datetime = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(verbose_name='Имя файла', max_length=50)


class Points(models.Model):
    customer = models.ForeignKey(Customer, verbose_name='Покупатель', on_delete=models.PROTECT)
    partner = models.ForeignKey(Partner, verbose_name='Партнер', on_delete=models.PROTECT)
    points_amount = models.IntegerField(verbose_name='Количество бонусов')
    receipt = models.ForeignKey(SellReceipt, verbose_name='Чек', on_delete=models.PROTECT)
    receive_or_spend = models.CharField(verbose_name='Списание или начисление', max_length=10)

    class Meta:
        verbose_name = 'Бонусы'
        verbose_name_plural = 'Бонусы'


class BaseLoyaltySystem(models.Model):
    partner = models.ForeignKey(Partner, verbose_name='Партнер', on_delete=models.PROTECT, unique=True)
    points_achieve = models.IntegerField(verbose_name='% начисляемых бонусов')
    points_spend = models.IntegerField(verbose_name='% стоимости товара для оплаты бонусами')

    class Meta:
        verbose_name = 'Базовая система лояльности'
        verbose_name_plural = 'Базовые системы лояльности'
