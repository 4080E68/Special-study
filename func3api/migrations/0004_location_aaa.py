# Generated by Django 3.2.8 on 2021-11-18 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('func3api', '0003_remove_location_asdress'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='aaa',
            field=models.CharField(default=123, max_length=100),
            preserve_default=False,
        ),
    ]
