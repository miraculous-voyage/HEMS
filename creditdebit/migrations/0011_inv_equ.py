# Generated by Django 2.0.7 on 2018-07-24 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditdebit', '0010_auto_20180724_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inv_equ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
            ],
        ),
    ]
