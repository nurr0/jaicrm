# Generated by Django 4.1.4 on 2022-12-17 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Jaimain", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="partner",
            options={
                "ordering": ["id"],
                "verbose_name": "Партнер",
                "verbose_name_plural": "Партнеры",
            },
        ),
        migrations.AlterField(
            model_name="partner",
            name="description",
            field=models.TextField(blank=True, verbose_name="Описание"),
        ),
        migrations.AlterField(
            model_name="partner",
            name="is_working",
            field=models.BooleanField(default=False, verbose_name="Активность"),
        ),
        migrations.AlterField(
            model_name="partner",
            name="logo",
            field=models.ImageField(upload_to="logos/", verbose_name="Логотип"),
        ),
        migrations.AlterField(
            model_name="partner",
            name="name",
            field=models.CharField(
                max_length=255, unique=True, verbose_name="Наименование партнера"
            ),
        ),
        migrations.AlterField(
            model_name="partner",
            name="partner_email",
            field=models.EmailField(max_length=254, verbose_name="Контактный email"),
        ),
        migrations.AlterField(
            model_name="partner",
            name="partner_tel",
            field=models.CharField(max_length=255, verbose_name="Контактный телефон"),
        ),
        migrations.AlterField(
            model_name="partner",
            name="time_create",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Время создания"
            ),
        ),
        migrations.AlterField(
            model_name="partner",
            name="time_expires",
            field=models.DateField(verbose_name="Дата окончания работы"),
        ),
        migrations.AlterField(
            model_name="partner",
            name="time_start_working",
            field=models.DateField(verbose_name="Дата начала работы"),
        ),
    ]
