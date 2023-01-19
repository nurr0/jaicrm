# Generated by Django 4.1.4 on 2023-01-18 13:30

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Наименование партнера')),
                ('logo', models.ImageField(upload_to='logos/', verbose_name='Логотип')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('iin', models.CharField(max_length=12, unique=True, verbose_name='ИИН/БИН')),
                ('partner_person', models.CharField(max_length=255, verbose_name='Контактное лицо')),
                ('partner_tel', models.CharField(max_length=255, verbose_name='Контактный телефон')),
                ('partner_email', models.EmailField(max_length=254, verbose_name='Контактный email')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('time_start_working', models.DateField(verbose_name='Дата начала работы')),
                ('time_expires', models.DateField(verbose_name='Дата окончания работы')),
                ('is_working', models.BooleanField(default=False, verbose_name='Активность')),
                ('receipt_prefix', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Префикс чека')),
            ],
            options={
                'verbose_name': 'Партнер',
                'verbose_name_plural': 'Партнеры',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'unique_together': 'Категория с таким же названием и родительской категорией уже существует'}, max_length=255, verbose_name='Наименование категории')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='Описание')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='Jaimain.productcategory', verbose_name='Родительская категория')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.partner', verbose_name='Партнер')),
            ],
            options={
                'verbose_name': 'Товарная категория',
                'verbose_name_plural': 'Товарные категории',
                'unique_together': {('partner', 'name', 'parent')},
            },
        ),
        migrations.CreateModel(
            name='ProductInStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Количество')),
            ],
        ),
        migrations.CreateModel(
            name='ProductProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование свойства')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Jaimain.partner', verbose_name='Партнер')),
            ],
            options={
                'verbose_name': 'Свойство товара',
                'verbose_name_plural': 'Свойства товаров',
                'unique_together': {('partner', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Наименование торговой точки')),
                ('location', models.CharField(max_length=255, unique=True, verbose_name='Адрес')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('is_working', models.BooleanField(default=True, verbose_name='Активность')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.partner', verbose_name='Партнер')),
            ],
            options={
                'verbose_name': 'Торговая точка',
                'verbose_name_plural': 'Торговые точки',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='JaiUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('tel_number', models.CharField(max_length=255, verbose_name='Контактный телефон')),
                ('is_costumer', models.BooleanField(default=False, verbose_name='Является покупателем')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('partner', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='Jaimain.partner', verbose_name='Партнер')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier', models.CharField(max_length=255, verbose_name='Поставщик')),
                ('document', models.CharField(max_length=255, verbose_name='Документ')),
                ('date', models.DateField(verbose_name='Дата')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.partner', verbose_name='Партнер')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.shop', verbose_name='Торговая точка')),
            ],
            options={
                'unique_together': {('supplier', 'document')},
            },
        ),
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='product_images/', verbose_name='Изображение')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='Описание')),
                ('identifier', models.CharField(max_length=255, unique=True, verbose_name='Артикул')),
                ('producer', models.CharField(max_length=255, verbose_name='Производитель')),
                ('category', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.productcategory', verbose_name='Категория')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Jaimain.partner', verbose_name='Партнер')),
            ],
            options={
                'verbose_name': 'SKU',
                'verbose_name_plural': 'SKU',
                'unique_together': {('partner', 'identifier', 'name')},
            },
        ),
        migrations.CreateModel(
            name='SellReceipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время регистрации чека')),
                ('number', models.IntegerField(verbose_name='Номер чека')),
                ('is_returned', models.BooleanField(default=False, verbose_name='Возврат')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.partner', verbose_name='Партнер')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.shop', verbose_name='Торговая точка')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'unique_together': {('partner', 'number')},
            },
        ),
        migrations.CreateModel(
            name='ProductsRemove',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decrease_amount', models.IntegerField(verbose_name='Количество')),
                ('reason', models.CharField(max_length=255, verbose_name='Основание')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.productinstock', verbose_name='Товар')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.shop', verbose_name='Склад')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductsInSupply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Количество')),
                ('product_supply_price', models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Закупочная стоимость')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.sku', verbose_name='Товар')),
                ('supply', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.supply', verbose_name='Поставка')),
            ],
        ),
        migrations.AddField(
            model_name='productinstock',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.sku', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='productinstock',
            name='shop',
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
        migrations.CreateModel(
            name='ProductPropertyRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='Значение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Jaimain.sku', verbose_name='SKU')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Jaimain.productproperty', verbose_name='Свойство')),
            ],
            options={
                'verbose_name': 'Связь свойства и товара',
                'verbose_name_plural': 'Связи свойств и товаров',
                'unique_together': {('product', 'property')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='productinstock',
            unique_together={('product', 'shop')},
        ),
        migrations.CreateModel(
            name='ProductInReceipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Количество')),
                ('price_in_stock', models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Установленная цена')),
                ('discount', models.IntegerField(blank=True, default=0, verbose_name='Скидка')),
                ('price_with_discount', models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Цена с учетом скидки')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.productinstock', verbose_name='Товар')),
                ('receipt', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Jaimain.sellreceipt', verbose_name='Чек')),
            ],
            options={
                'unique_together': {('receipt', 'product')},
            },
        ),
    ]
