# Generated by Django 3.2.12 on 2022-03-30 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockCenterLine', '0004_alter_setting_selected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='selected',
            field=models.CharField(max_length=100, verbose_name='선택여부'),
        ),
    ]
