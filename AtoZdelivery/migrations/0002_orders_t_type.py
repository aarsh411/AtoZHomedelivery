# Generated by Django 2.0.2 on 2019-03-19 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AtoZdelivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='t_type',
            field=models.CharField(default=' ', max_length=20),
        ),
    ]