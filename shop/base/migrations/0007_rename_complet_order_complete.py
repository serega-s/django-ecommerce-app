# Generated by Django 3.2.5 on 2021-07-22 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_customer_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='complet',
            new_name='complete',
        ),
    ]