# Generated by Django 3.1.4 on 2021-01-04 06:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0008_auto_20210103_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 6, 6, 38, 32, 155651, tzinfo=utc)),
        ),
    ]
