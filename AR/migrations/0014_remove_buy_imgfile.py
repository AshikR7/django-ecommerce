# Generated by Django 4.1.6 on 2023-02-21 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AR', '0013_buy_customercard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buy',
            name='imgfile',
        ),
    ]