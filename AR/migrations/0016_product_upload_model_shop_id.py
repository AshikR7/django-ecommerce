# Generated by Django 4.1.6 on 2023-03-28 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AR', '0015_alter_customercard_cardexpiry_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_upload_model',
            name='shop_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
