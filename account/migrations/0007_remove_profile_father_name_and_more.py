# Generated by Django 5.1.4 on 2025-01-03 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='father_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='national_code',
        ),
        migrations.AddField(
            model_name='profile',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
    ]
