# Generated by Django 4.1.2 on 2022-10-31 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_store_image_alter_inventory_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='nickname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
