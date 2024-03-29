# Generated by Django 5.0.3 on 2024-03-09 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ai_news", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="body",
            new_name="comment",
        ),
        migrations.RenameField(
            model_name="comment",
            old_name="author",
            new_name="publisher",
        ),
        migrations.AddField(
            model_name="article",
            name="url",
            field=models.URLField(default=""),
        ),
        migrations.AlterField(
            model_name="article",
            name="pub_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="publisher",
            name="date_of_registration",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
