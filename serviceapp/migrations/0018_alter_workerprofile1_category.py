# Generated by Django 4.2.6 on 2024-01-05 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapp', '0017_booking_approval_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workerprofile1',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='serviceapp.servicecategory'),
        ),
    ]