# Generated by Django 4.2.6 on 2023-11-27 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapp', '0003_remove_booking_status_booking_is_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='is_approved',
        ),
        migrations.CreateModel(
            name='Notificationservice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceapp.workerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Booking1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField(default=False)),
                ('booking', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='serviceapp.booking')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='serviceapp.service')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='serviceapp.userprofile')),
            ],
        ),
    ]
