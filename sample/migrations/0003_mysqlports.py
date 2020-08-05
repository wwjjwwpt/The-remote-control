# Generated by Django 2.0 on 2020-08-02 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sample', '0002_springports'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mysqlports',
            fields=[
                ('port', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='生成日期')),
                ('state', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
