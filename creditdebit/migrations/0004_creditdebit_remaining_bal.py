# Generated by Django 2.0.7 on 2018-07-22 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditdebit', '0003_auto_20180722_0157'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditdebit',
            name='remaining_bal',
            field=models.IntegerField(default=0),
        ),
    ]
