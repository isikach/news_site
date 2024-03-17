# Generated by Django 5.0.3 on 2024-03-16 21:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ai_news", "0008_remove_publisher_pseudonym"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="articles_liked", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
