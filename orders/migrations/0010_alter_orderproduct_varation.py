# Generated by Django 4.0.4 on 2022-06-15 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0031_discount'),
        ('orders', '0009_remove_orderproduct_size_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='varation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.variation'),
        ),
    ]