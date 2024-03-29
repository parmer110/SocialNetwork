# Generated by Django 4.1.5 on 2023-03-28 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0014_comment_like_likeunlike_likechange_likeunlike_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='user',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='like',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
