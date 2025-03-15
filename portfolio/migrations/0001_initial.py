# Generated by Django 5.1.7 on 2025-03-11 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('owner_of_portfolio', models.CharField(max_length=50)),
                ('geographic_region', models.CharField(max_length=50)),
            ],
        ),
    ]
