# Generated by Django 3.1 on 2020-10-05 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groceries_app', '0006_ingredientquantity_optional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='gallery'),
        ),
    ]