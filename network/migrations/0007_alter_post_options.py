# Generated by Django 4.1.5 on 2023-03-28 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_alter_user_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('timestamp',)},
        ),
    ]
