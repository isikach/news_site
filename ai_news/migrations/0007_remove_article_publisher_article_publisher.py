# Generated by Django 5.0.3 on 2024-03-13 20:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_news', '0006_alter_publisher_pseudonym'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='publisher',
        ),
        migrations.AddField(
            model_name='article',
            name='publisher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
