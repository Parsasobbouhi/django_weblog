# Generated by Django 5.1.4 on 2025-01-02 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='images/user.png', null=True, upload_to='images/profiles'),
        ),
    ]