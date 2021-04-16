# Generated by Django 2.2.6 on 2019-11-19 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_auto_20191107_0734'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Item Settings', max_length=50)),
                ('low_stock_limit', models.IntegerField(default=10)),
                ('item_expiration_limit', models.IntegerField(choices=[(30, '1 Months'), (60, '2 Months'), (90, '3 Months'), (120, '4 Months')], default=30)),
            ],
            options={
                'verbose_name': 'Item Setting',
                'verbose_name_plural': 'Item Settings',
            },
        ),
    ]
