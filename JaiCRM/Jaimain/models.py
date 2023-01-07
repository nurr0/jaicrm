from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F
from django.urls import reverse
from django.utils.safestring import mark_safe
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from mptt.models import MPTTModel, TreeForeignKey


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

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
        ordering = ['id']

    def __str__(self):
        return self.name


class JaiUser(AbstractUser):
    partner = models.ForeignKey('Partner', on_delete=models.PROTECT, verbose_name="Партнер", default=None, null=True)
    tel_number = models.CharField(max_length=255, verbose_name='Контактный телефон')
    is_costumer = models.BooleanField(default=False, verbose_name='Является покупателем', null=False, blank=False)

    def __str__(self):
        return self.username


class Shop(models.Model):
    partner = models.ForeignKey('Partner', on_delete=models.PROTECT, verbose_name="Партнер", null=False)
    name = models.CharField(max_length=255, unique=True, verbose_name='Наименование торговой точки')
    location = models.CharField(max_length=255, unique=True, verbose_name='Адрес')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_working = models.BooleanField(default=True, verbose_name='Активность')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

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

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('partner', 'name'),)
        verbose_name = 'Свойство товара'
        verbose_name_plural = 'Свойства товаров'


class SKU(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование', blank=False, null=False)
    image = models.ImageField(upload_to=f'product_images/', verbose_name='Изображение', blank=True, default=None, null=True)
    description = models.TextField(blank=True, verbose_name='Описание', default=None, null=True)
    identifier = models.CharField(blank=False, max_length=255, null=False, verbose_name='Артикул', unique=True)
    producer = models.CharField(blank=False, max_length=255, null=False, verbose_name='Производитель')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name='Партнер')
    category = TreeForeignKey(ProductCategory, on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return f'{self.identifier}/{self.name}'

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
