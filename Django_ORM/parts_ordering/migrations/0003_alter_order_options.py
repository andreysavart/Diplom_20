# Generated by Django 5.1.1 on 2024-09-11 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parts_ordering', '0002_alter_boltjoint_options_alter_order_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at'], 'verbose_name': 'заказ', 'verbose_name_plural': 'заказы'},
        ),
    ]
