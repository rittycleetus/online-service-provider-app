# Generated by Django 4.2.6 on 2023-11-29 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapp', '0008_booking_is_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='serviceapp.workerprofile'),
        ),
    ]
