# Generated by Django 3.0.5 on 2021-04-22 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210422_0152'),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='total_payment',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
