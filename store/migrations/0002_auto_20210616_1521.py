# Generated by Django 3.2.4 on 2021-06-16 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='title',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='color',
            name='title',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='idealfor',
            name='title',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='nacktype',
            name='title',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='occasion',
            name='title',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='sleeve',
            name='title',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='tshirt',
            name='title',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]