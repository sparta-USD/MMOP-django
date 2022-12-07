# Generated by Django 4.1.3 on 2022-12-06 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_perfume', '0001_initial'),
        ('perfume', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfume',
            name='base_notes',
        ),
        migrations.RemoveField(
            model_name='perfume',
            name='heart_notes',
        ),
        migrations.RemoveField(
            model_name='perfume',
            name='none_notes',
        ),
        migrations.RemoveField(
            model_name='perfume',
            name='top_notes',
        ),
        migrations.AddField(
            model_name='perfume',
            name='base_notes',
            field=models.ManyToManyField(blank=True, related_name='perfumes_base', to='custom_perfume.note'),
        ),
        migrations.AddField(
            model_name='perfume',
            name='heart_notes',
            field=models.ManyToManyField(blank=True, related_name='perfumes_heart', to='custom_perfume.note'),
        ),
        migrations.AddField(
            model_name='perfume',
            name='none_notes',
            field=models.ManyToManyField(blank=True, related_name='perfumes_none', to='custom_perfume.note'),
        ),
        migrations.AddField(
            model_name='perfume',
            name='top_notes',
            field=models.ManyToManyField(blank=True, related_name='perfumes_top', to='custom_perfume.note'),
        ),
    ]
