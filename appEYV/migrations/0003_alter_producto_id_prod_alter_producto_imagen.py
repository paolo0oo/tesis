# Generated by Django 4.2.2 on 2024-11-06 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appEYV', '0002_producto_imagen_producto_nombre_prod_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='ID_prod',
            field=models.CharField(max_length=3, unique=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='Imagen',
            field=models.ImageField(blank=True, null=True, upload_to='img/'),
        ),
    ]