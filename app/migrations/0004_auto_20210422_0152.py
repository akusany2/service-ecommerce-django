# Generated by Django 3.0.5 on 2021-04-22 00:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210421_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clients',
            name='user',
        ),
        migrations.AddField(
            model_name='clients',
            name='serviceId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ServiceMenu'),
        ),
    ]
