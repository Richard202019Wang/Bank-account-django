# Generated by Django 4.1.2 on 2022-10-30 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('banks', '0006_alter_bank_bank'),
    ]

    operations = [
        migrations.RenameField(
            model_name='branch',
            old_name='transit_number',
            new_name='transit_num',
        ),
        migrations.AlterField(
            model_name='bank',
            name='bank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
