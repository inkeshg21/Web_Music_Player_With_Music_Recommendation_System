# Generated by Django 4.1.5 on 2023-02-19 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_profile_forgot_password_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]