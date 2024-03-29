# Generated by Django 2.2.6 on 2019-11-21 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0010_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeitem',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='items.Category'),
        ),
        migrations.AddField(
            model_name='storeitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
