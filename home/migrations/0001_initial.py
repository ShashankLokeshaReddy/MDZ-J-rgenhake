# Generated by Django 4.2.7 on 2024-02-26 19:51

import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import home.models
import home.storage
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Akkuvariante',
            fields=[
                ('akkuvariante_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('akkuvariante_image_path', models.ImageField(default='default.png', storage=home.storage.OverwriteStorage(), upload_to=home.models.get_img_upload_path_akku)),
            ],
            options={
                'verbose_name': 'Akkuvariante',
                'verbose_name_plural': 'Akkuvarianten',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('color_name', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Kategorie')),
                ('color_value', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=25, samples=None, verbose_name='Farbcode')),
            ],
            options={
                'verbose_name': 'Farbe',
                'verbose_name_plural': 'Farben',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('general_image_name', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Bezeichnung')),
                ('general_image_path', models.ImageField(default='default.png', storage=home.storage.OverwriteStorage(), upload_to=home.models.get_img_upload_path_general_images, verbose_name='Abbildungspfad')),
            ],
            options={
                'verbose_name': 'Abbildung',
                'verbose_name_plural': 'Abbildungen',
            },
        ),
        migrations.CreateModel(
            name='InCartItem',
            fields=[
                ('item_nummer', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Artikelnummer')),
                ('benutzername', models.CharField(max_length=50, null=True)),
                ('akkuvariante', models.CharField(max_length=255, null=True)),
                ('mit_120_Ohm_CAN_Bus_Widerstand', models.CharField(choices=[('Ja', 'Ja'), ('Nein', 'Nein')], default='Nein', max_length=255, null=True)),
                ('kabelvariante', models.CharField(max_length=255, null=True)),
                ('schnittstelle', models.CharField(max_length=255, null=True)),
                ('masse', models.CharField(max_length=255, null=True, verbose_name='Maße')),
                ('menge', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('original_preis', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Originalpreis')),
                ('reduzierter_preis', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Reduzierter Preis')),
                ('gesamt', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'verbose_name': 'Artikel im Warenkorb',
                'verbose_name_plural': 'Artikel im Warenkorb',
            },
        ),
        migrations.CreateModel(
            name='Kabelvariante',
            fields=[
                ('kabelvariante_name', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Kabelvariante')),
                ('kabelvariante_image_path', models.ImageField(default='default.png', storage=home.storage.OverwriteStorage(), upload_to=home.models.get_img_upload_path_kabel, verbose_name='Abbildungspfad')),
                ('main_part_min_length', models.IntegerField(null=True, verbose_name='Mindestlänge der Hauptleitung')),
                ('split_part_min_length', models.IntegerField(null=True, verbose_name='Mindestlänge der Zweigleitungen')),
                ('masse_image_path', models.ImageField(default='default.png', storage=home.storage.OverwriteStorage(), upload_to=home.models.get_img_upload_path_masse, verbose_name='Abbildungspfad für beschriftete Abbildung')),
                ('splits', models.IntegerField(null=True, verbose_name='Splits')),
            ],
            options={
                'verbose_name': 'Kabelvariante',
                'verbose_name_plural': 'Kabelvarianten',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_nummer', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Bestellnummer')),
                ('benutzername', models.CharField(max_length=50, null=True)),
                ('order_datum', models.DateTimeField(auto_now_add=True)),
                ('bestelldetails', models.CharField(max_length=255, null=True)),
                ('order_status', models.CharField(choices=[('Angebot angefordert', 'Angebot angefordert'), ('Bestellt', 'Bestellt'), ('Geliefert', 'Geliefert'), ('Abgesagt', 'Abgesagt')], default='Bestellt', max_length=255, null=True, verbose_name='Bestellstatus')),
            ],
            options={
                'verbose_name': 'Bestellung',
                'verbose_name_plural': 'Bestellungen',
            },
        ),
        migrations.CreateModel(
            name='PreisListe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kabelvariante', models.CharField(max_length=50, null=True)),
                ('gehause', models.CharField(max_length=50, null=True, verbose_name='Akkuvariante')),
                ('leitung', models.CharField(max_length=50, null=True, verbose_name='Schnittstelle')),
                ('lange', models.CharField(max_length=50, null=True, verbose_name='Länge')),
                ('qty_1', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('qty_25', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('qty_50', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('qty_100', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('qty_250', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('qty_500', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('qty_1000', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('qty_2000', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'verbose_name': 'Preis',
                'verbose_name_plural': 'Preisliste',
            },
        ),
        migrations.CreateModel(
            name='Schnittstelle',
            fields=[
                ('schnittstelle_name', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Bezeichnung')),
                ('schnittstelle_image_path', models.ImageField(default='default.png', storage=home.storage.OverwriteStorage(), upload_to=home.models.get_img_upload_path_schnittstelle, verbose_name='Abbildungspfad')),
            ],
            options={
                'verbose_name': 'Schnittstelle',
                'verbose_name_plural': 'Schnittstellen',
            },
        ),
        migrations.CreateModel(
            name='SpezielleBestellung',
            fields=[
                ('order_nummer', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Bestellnummer')),
                ('Ust_id', models.CharField(max_length=255, null=True)),
                ('order_datum', models.DateTimeField(auto_now_add=True, null=True)),
                ('Status', models.CharField(choices=[('Bestellt', 'Bestellt'), ('Geliefert', 'Geliefert'), ('Abgesagt', 'Abgesagt')], default='InCart', max_length=255, null=True)),
                ('hochgeladene_datei', models.FileField(null=True, upload_to='special_orders/', verbose_name='Hochgeladene Datei')),
            ],
            options={
                'verbose_name': 'Sonderlösung',
                'verbose_name_plural': 'Sonderlösungen',
            },
        ),
        migrations.CreateModel(
            name='UILabel',
            fields=[
                ('label_key', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Label')),
                ('label_value', models.CharField(max_length=1000, null=True, verbose_name='Labelwert')),
            ],
            options={
                'verbose_name': 'UI-Label',
                'verbose_name_plural': 'UI-Labels',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('item_nummer', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Artikelnummer')),
                ('benutzername', models.CharField(max_length=50, null=True)),
                ('mit_120_Ohm_CAN_Bus_Widerstand', models.CharField(choices=[('Ja', 'Ja'), ('Nein', 'Nein')], default='Nein', max_length=255, null=True)),
                ('akkuvariante', models.CharField(max_length=255, null=True)),
                ('kabelvariante', models.CharField(max_length=255, null=True)),
                ('schnittstelle', models.CharField(max_length=255, null=True)),
                ('masse', models.CharField(max_length=255, null=True, verbose_name='Maße')),
                ('menge', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('original_preis', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Originalpreis')),
                ('reduzierter_preis', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Reduzierter Preis')),
                ('gesamt', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('order', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='home.order', verbose_name='Bestellung')),
            ],
            options={
                'verbose_name': 'Bestellten Artikel',
                'verbose_name_plural': 'Bestellte Artikel',
            },
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('benutzername', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('ust_id', models.CharField(max_length=20, null=True)),
                ('image', models.ImageField(default='General/default.png', storage=home.storage.OverwriteStorage(), upload_to=home.models.get_img_upload_path_profile)),
                ('unternehmensname', models.CharField(max_length=255, null=True)),
                ('land', models.CharField(max_length=100, null=True)),
                ('adresse', models.TextField(null=True)),
                ('plz', models.CharField(max_length=5, null=True)),
                ('telefonnummer', models.CharField(max_length=20, null=True)),
                ('ansprechpartner', models.CharField(max_length=255, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Kundenprofil',
                'verbose_name_plural': 'Kundenprofile',
            },
        ),
    ]
