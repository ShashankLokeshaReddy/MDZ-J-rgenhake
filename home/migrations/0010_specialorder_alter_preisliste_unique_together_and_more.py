# Generated by Django 4.2.7 on 2024-01-27 16:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_preisliste_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialOrder',
            fields=[
                ('order_nummer', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('Ust_Id', models.CharField(max_length=255, null=True)),
                ('order_datum', models.DateTimeField(auto_now_add=True, null=True)),
                ('Status', models.CharField(choices=[('InCart', 'InCart'), ('Bestellt', 'Bestellt'), ('Geliefert', 'Geliefert'), ('Abgesagt', 'Abgesagt')], default='InCart', max_length=255, null=True)),
                ('hochgeladene_datei', models.FileField(null=True, upload_to='special_orders/')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='order_datum',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
