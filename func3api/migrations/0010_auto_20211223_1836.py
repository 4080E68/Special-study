# Generated by Django 3.2.8 on 2021-12-23 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('func3api', '0009_auto_20211214_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='display',
            name='pc_images',
            field=models.CharField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='display',
            name='price',
            field=models.IntegerField(max_length=500),
        ),
    ]
