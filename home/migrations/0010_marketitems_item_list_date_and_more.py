# Generated by Django 5.2.1 on 2025-06-14 03:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_farmerhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketitems',
            name='item_list_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='marketitems',
            name='location',
            field=models.CharField(default='Neelbad, Bhopal, Mp-42603', max_length=300),
        ),
    ]
