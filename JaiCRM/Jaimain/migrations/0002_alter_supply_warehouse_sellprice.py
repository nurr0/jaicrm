# Generated by Django 4.1.4 on 2023-01-15 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Jaimain', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supply',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.shop', verbose_name='Торговая точка'),
        ),
        migrations.CreateModel(
            name='SellPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Цена')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.partner', verbose_name='Партнер')),
                ('product_in_stock', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.productinstock', verbose_name='Товар')),
            ],
            options={
                'unique_together': {('product_in_stock', 'partner')},
            },
        ),
    ]