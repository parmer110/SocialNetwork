# Generated by Django 4.1.5 on 2023-03-28 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='postedition',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
