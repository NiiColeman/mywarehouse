# Generated by Django 2.2.6 on 2019-11-07 15:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_item_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
