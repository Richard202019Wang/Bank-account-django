# Generated by Django 4.1.2 on 2022-10-30 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banks', '0008_alter_branch_last_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
