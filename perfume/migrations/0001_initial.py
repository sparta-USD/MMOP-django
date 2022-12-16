# Generated by Django 4.1.3 on 2022-12-16 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import perfume.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('custom_perfume', '0004_alter_customperfume_logo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('image', models.CharField(blank=True, max_length=256, null=True)),
                ('title', models.CharField(max_length=100)),
                ('website', models.CharField(blank=True, max_length=256, null=True)),
                ('brand_desc', models.TextField(blank=True, null=True)),
                ('brand_desc_ko', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Perfume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.IntegerField()),
                ('image', models.CharField(blank=True, max_length=256, null=True)),
                ('title', models.CharField(max_length=100)),
                ('gender', models.CharField(blank=True, max_length=5, null=True)),
                ('price', models.FloatField(default=0)),
                ('price_unit', models.CharField(blank=True, default='USD', max_length=100, null=True)),
                ('launch_date', models.DateField(blank=True, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('desc_ko', models.TextField(blank=True, null=True)),
                ('base_notes', models.ManyToManyField(blank=True, related_name='perfumes_base', to='custom_perfume.note')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brand_perfume', to='perfume.brand')),
                ('heart_notes', models.ManyToManyField(blank=True, related_name='perfumes_heart', to='custom_perfume.note')),
                ('likes', models.ManyToManyField(blank=True, related_name='like_perfume', to=settings.AUTH_USER_MODEL)),
                ('none_notes', models.ManyToManyField(blank=True, related_name='perfumes_none', to='custom_perfume.note')),
                ('top_notes', models.ManyToManyField(blank=True, related_name='perfumes_top', to='custom_perfume.note')),
            ],
            options={
                'verbose_name': '향수',
                'verbose_name_plural': '향수 제품',
                'db_table': 'perfume',
                'ordering': ['-launch_date', 'brand', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('good_content', models.TextField(blank=True, default='')),
                ('bad_content', models.TextField(blank=True, default='')),
                ('grade', models.FloatField(blank=True, default=5)),
                ('survey', models.BooleanField(blank=True, default=False)),
                ('image', models.ImageField(max_length=255, null=True, upload_to=perfume.models.rename_reviewimage)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('perfume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perfume_reviews', to='perfume.perfume')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
