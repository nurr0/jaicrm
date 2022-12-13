from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/')
    description = models.TextField(blank=True)
    partner_tel = models.CharField(max_length=255)
    partner_email = models.EmailField()
    partner_person = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)
    time_start_working = models.DateField()
    time_expires = models.DateField()
    is_working = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
        ordering = ['id']
