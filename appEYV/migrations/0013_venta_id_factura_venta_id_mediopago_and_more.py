# Generated by Django 4.2.2 on 2024-12-09 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appEYV', '0012_remove_venta_id_factura_remove_venta_id_mediopago_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='ID_Factura',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='venta',
            name='ID_mediopago',
            field=models.CharField(default='0.0', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venta',
            name='ID_producto',
            field=models.DecimalField(decimal_places=2, default='0.0', max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='venta',
            name='Comprobante',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='venta',
            name='DetalleVenta',
            field=models.CharField(max_length=255),
        ),
    ]
