# Generated by Django 5.1.4 on 2025-02-03 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_phone',
            field=models.BigIntegerField(),
        ),
    ]
