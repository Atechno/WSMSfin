# Generated by Django 3.1a1 on 2020-12-02 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('esp', '0004_sensordata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensordata',
            name='sensorId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='esp.sensorreg'),
        ),
    ]
