# Generated by Django 2.0.7 on 2018-07-22 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('creditdebit', '0007_creditdebit_last_edited_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditdebit',
            name='transaction_type',
        ),
    ]
