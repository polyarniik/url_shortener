# Generated by Django 3.2.12 on 2022-05-19 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='URL')),
                ('short_url', models.URLField(verbose_name='Short URL')),
                ('visits_count', models.IntegerField(default=0, verbose_name='Visits count')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urls', to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('created_at', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created time')),
            ],
        ),
    ]
