# Generated by Django 5.1.4 on 2025-01-03 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_profile_linkedin'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='github',
            field=models.URLField(blank=True, null=True),
        ),
    ]
