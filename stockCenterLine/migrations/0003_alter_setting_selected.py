# Generated by Django 3.2.12 on 2022-03-30 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockCenterLine', '0002_auto_20220329_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='selected',
            field=models.CharField(max_length=50, verbose_name='선택여부'),
        ),
    ]
