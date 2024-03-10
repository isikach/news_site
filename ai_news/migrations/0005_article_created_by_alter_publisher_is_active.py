# Generated by Django 5.0.3 on 2024-03-10 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_news', '0004_alter_comment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='created_by',
            field=models.CharField(choices=[('from_url', 'from_url'), ('from_user', 'from_user')], default='from_user', max_length=10),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
