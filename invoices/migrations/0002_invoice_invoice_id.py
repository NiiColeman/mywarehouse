# Generated by Django 2.2.6 on 2019-11-12 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='invoice_id',
            field=models.CharField(blank=True, max_length=250, unique=True),
        ),
    ]
