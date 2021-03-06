# Generated by Django 3.0.8 on 2020-07-11 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('supplier_id', models.AutoField(primary_key=True, serialize=False)),
                ('supplier_name', models.CharField(max_length=200)),
                ('contact_firstName', models.CharField(max_length=200)),
                ('contact_lastName', models.CharField(max_length=200)),
                ('contact_title', models.CharField(max_length=200)),
                ('supplier_address1', models.CharField(max_length=200)),
                ('supplier_address2', models.CharField(max_length=200, null=True)),
                ('supplier_city', models.CharField(max_length=200)),
                ('supplier_state', models.CharField(max_length=2)),
                ('supplier_country', models.CharField(max_length=200)),
                ('supplier_email', models.EmailField(max_length=254)),
                ('supplier_website', models.URLField()),
            ],
            options={
                'verbose_name': 'supplier',
                'verbose_name_plural': 'suppliers',
                'db_table': 'suppliers',
            },
        ),
        migrations.CreateModel(
            name='Tops',
            fields=[
                ('product_sku', models.CharField(db_index=True, max_length=50, unique=True)),
                ('product_name', models.CharField(max_length=50)),
                ('product_color', models.CharField(max_length=50)),
                ('product_shortDesc', models.CharField(blank=True, max_length=50)),
                ('product_longDesc', models.CharField(blank=True, max_length=50)),
                ('product_price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('product_weight', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('slug', models.SlugField(unique=True)),
                ('added_date', models.DateField()),
                ('top_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_type', models.CharField(choices=[('TE', 'Tee'), ('SH', 'Shirt'), ('TT', 'Tank Top'), ('HO', 'Hoody'), ('KR', 'Kurta')], max_length=2)),
                ('product_size', models.CharField(choices=[('XS', 'Extra Small'), ('SM', 'Small'), ('MD', 'Medium'), ('LG', 'Large'), ('XL', 'Extra Large')], default='NA', max_length=2)),
                ('product_image', models.ImageField(upload_to='Tops/')),
                ('supplier', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='inventory.Suppliers')),
            ],
            options={
                'verbose_name': 'top',
                'verbose_name_plural': 'tops',
                'db_table': 'tops',
            },
        ),
        migrations.CreateModel(
            name='Shoes',
            fields=[
                ('product_sku', models.CharField(db_index=True, max_length=50, unique=True)),
                ('product_name', models.CharField(max_length=50)),
                ('product_color', models.CharField(max_length=50)),
                ('product_shortDesc', models.CharField(blank=True, max_length=50)),
                ('product_longDesc', models.CharField(blank=True, max_length=50)),
                ('product_price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('product_weight', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('slug', models.SlugField(unique=True)),
                ('added_date', models.DateField()),
                ('shoe_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_image', models.ImageField(upload_to='Shoes')),
                ('product_size', models.CharField(choices=[('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13')], default='NA', max_length=2)),
                ('supplier', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='inventory.Suppliers')),
            ],
            options={
                'verbose_name': 'shoe',
                'verbose_name_plural': 'shoes',
                'db_table': 'shoes',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('inventory_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_count', models.IntegerField(default=0)),
                ('product_cost', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('added_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Bottoms',
            fields=[
                ('product_sku', models.CharField(db_index=True, max_length=50, unique=True)),
                ('product_name', models.CharField(max_length=50)),
                ('product_color', models.CharField(max_length=50)),
                ('product_shortDesc', models.CharField(blank=True, max_length=50)),
                ('product_longDesc', models.CharField(blank=True, max_length=50)),
                ('product_price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('product_weight', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('slug', models.SlugField(unique=True)),
                ('added_date', models.DateField()),
                ('bottom_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_type', models.CharField(choices=[('PA', 'Pants'), ('PJ', 'Pajama'), ('SO', 'Shorts')], default='NA', max_length=2)),
                ('product_size', models.CharField(choices=[('XS', 'Extra Small'), ('SM', 'Small'), ('MD', 'Medium'), ('LG', 'Large'), ('XL', 'Extra Large')], default='NA', max_length=2)),
                ('product_image', models.ImageField(upload_to='Bottoms/')),
                ('supplier', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='inventory.Suppliers')),
            ],
            options={
                'verbose_name': 'bottom',
                'verbose_name_plural': 'bottoms',
                'db_table': 'bottoms',
            },
        ),
        migrations.CreateModel(
            name='Accessories',
            fields=[
                ('product_sku', models.CharField(db_index=True, max_length=50, unique=True)),
                ('product_name', models.CharField(max_length=50)),
                ('product_color', models.CharField(max_length=50)),
                ('product_shortDesc', models.CharField(blank=True, max_length=50)),
                ('product_longDesc', models.CharField(blank=True, max_length=50)),
                ('product_price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('product_weight', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('slug', models.SlugField(unique=True)),
                ('added_date', models.DateField()),
                ('accessory_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_type', models.CharField(default=[('AC', 'accessories')], max_length=2)),
                ('product_image', models.ImageField(upload_to='accessories/')),
                ('supplier', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='inventory.Suppliers')),
            ],
            options={
                'verbose_name': 'accessory',
                'verbose_name_plural': 'accessories',
                'db_table': 'accessories',
            },
        ),
    ]
