# Generated by Django 3.1 on 2020-09-22 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groceries_app', '0002_auto_20200922_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientquantity',
            name='quantity',
            field=models.FloatField(),
        ),
    ]
