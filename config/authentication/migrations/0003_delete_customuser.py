# Generated by Django 5.1.1 on 2024-10-22 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
