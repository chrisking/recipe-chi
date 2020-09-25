# Generated by Django 3.1 on 2020-09-22 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groceries_app', '0003_auto_20200922_0035'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='specialty',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='specialty_location',
            field=models.CharField(blank=True, choices=[('vegan', 'Vegan Specialty'), ('indian', 'Indian Grocery'), ('asian', 'Asian Grocery'), ('ethiopian', 'Ethiopian Grocery')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='category',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]