# Generated by Django 4.2.7 on 2024-01-25 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_orderitem_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='preisliste',
            options={},
        ),
        migrations.AddField(
            model_name='incartitem',
            name='menge',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='masse',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='incartitem',
            name='masse',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Ordered', 'Ordered'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Ordered', max_length=255, null=True),
        ),
    ]
