# Generated by Django 3.2.4 on 2021-06-17 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_tshirt_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tshirt',
            name='discount',
            field=models.IntegerField(default=0),
        ),
    ]