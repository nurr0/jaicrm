from django.contrib.auth.models import AbstractUser
from django.db import models


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
    is_costumer = models.BooleanField(default=False, verbose_name='Является покупателем')


class Shop(models.Model):
    partner = models.ForeignKey('Partner', on_delete=models.PROTECT, verbose_name="Партнер", default=None, null=False)
    name = models.CharField(max_length=255, unique=True, verbose_name='Наименование торговой точки')
    location = models.CharField(max_length=255, unique=True, verbose_name='Адрес')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_working = models.BooleanField(default=True, verbose_name='Активность')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Торговая точка'
        verbose_name_plural = 'Торговые точки'
        ordering = ['id']
