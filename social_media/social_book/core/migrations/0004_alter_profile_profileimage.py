# Generated by Django 4.2.3 on 2023-08-03 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_profile_profileimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profileimage',
            field=models.ImageField(default='blank-profile-picture.png', upload_to='profile_images'),
        ),
    ]
