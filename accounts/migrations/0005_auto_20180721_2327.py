# Generated by Django 2.0.2 on 2018-07-21 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20180721_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extrainfo',
            name='user_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
