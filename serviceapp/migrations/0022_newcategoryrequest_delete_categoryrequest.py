# Generated by Django 4.2.6 on 2024-01-08 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapp', '0021_categoryrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewCategoryRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='CategoryRequest',
        ),
    ]
