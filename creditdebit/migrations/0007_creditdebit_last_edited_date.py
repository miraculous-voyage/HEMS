# Generated by Django 2.0.7 on 2018-07-22 17:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('creditdebit', '0006_auto_20180722_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditdebit',
            name='last_edited_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
