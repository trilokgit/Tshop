# Generated by Django 3.2.4 on 2021-06-18 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_tshirt_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tshirt',
            name='slug',
            field=models.CharField(default='', max_length=200, unique=True),
        ),
    ]
