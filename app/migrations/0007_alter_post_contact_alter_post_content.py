# Generated by Django 4.2.1 on 2023-12-10 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='contact',
            field=models.CharField(max_length=32, verbose_name='Контакты'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(verbose_name='Описание'),
        ),
    ]
