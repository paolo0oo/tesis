# Generated by Django 4.2.2 on 2024-12-09 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appEYV', '0013_venta_id_factura_venta_id_mediopago_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='ID_producto',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
