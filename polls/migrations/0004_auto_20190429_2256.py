# Generated by Django 2.2 on 2019-04-30 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20190420_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='DateOfBirth',
            field=models.DateField(),
        ),
    ]