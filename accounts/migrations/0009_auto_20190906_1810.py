# Generated by Django 2.2.4 on 2019-09-06 23:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20190906_1757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='reading',
        ),
        migrations.RemoveField(
            model_name='file',
            name='user',
        ),
    ]