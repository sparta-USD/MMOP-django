# Generated by Django 4.1.3 on 2022-12-16 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfume', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfume',
            name='title',
            field=models.CharField(max_length=256),
        ),
    ]