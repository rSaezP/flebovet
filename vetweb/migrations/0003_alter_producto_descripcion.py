# Generated by Django 4.2 on 2025-01-13 15:46

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vetweb', '0002_remove_producto_categoria_remove_producto_precio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
