# Generated by Django 4.1.5 on 2023-02-09 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
