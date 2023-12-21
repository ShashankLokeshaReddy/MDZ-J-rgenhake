# Generated by Django 4.2.7 on 2023-11-30 00:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0002_akkuvariante_alter_customerprofile_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerprofile',
            name='email',
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
