from django.db import migrations, models
from colorfield.fields import ColorField

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('ust_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('unternehmensname', models.CharField(max_length=255, null=True)),
                ('land', models.CharField(max_length=100, null=True)),
                ('address', models.TextField(null=True)),
                ('email', models.EmailField(null=True)),
                ('telefonnummer', models.CharField(max_length=20, null=True)),
                ('ansprechpartner', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Akkuvariante',
            fields=[
                ('akkuvariante_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('akkuvariante_image_path', models.ImageField(default='default.png', upload_to='Akkuvariante')),
                ('akkuvariante_price', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kabelvariante',
            fields=[
                ('kabelvariante_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('kabelvariante_image_path', models.ImageField(default='default.png', upload_to='Kabelvariante')),
                ('main_part_min_length', models.IntegerField(null=True)),
                ('main_part_max_length', models.IntegerField(null=True)),
                ('split_part_min_length', models.IntegerField(null=True)),
                ('split_part_max_length', models.IntegerField(null=True)),
                ('masse_image_path', models.ImageField(default='default.png', upload_to='Maße')),
                # ('schnittstelle_image_path', models.ImageField(default='default.png', upload_to='Maße')),
                ('splits', models.IntegerField(null=True)),
                ('kabel_price_per_meter', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Schnittstelle',
            fields=[
                ('schnittstelle_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('schnittstelle_image_path', models.ImageField(default='default.png', upload_to='Schnittstellen')),
                ('schnittstelle_price', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('color_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('color_value', ColorField(format="hex")),
            ],
        ),
        migrations.CreateModel(
            name='UILabel',
            fields=[
                ('label_key', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('label_value', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_path', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_number', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('ust_id', models.CharField(max_length=50, null=True)),
                ('order_date', models.DateTimeField(null=True)),
                ('order_details', models.CharField(max_length=255,null=True)),
                ('order_status', models.CharField(max_length=255,null=True)),
                ('quantity', models.FloatField(null=True)),
                ('price', models.FloatField(null=True)),
                ('total', models.FloatField(null=True)),
            ],
        ),
    ]
