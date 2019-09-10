# Generated by Django 2.2.4 on 2019-09-10 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_file_textracted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jreturns',
            name='file_name',
        ),
        migrations.RemoveField(
            model_name='jreturns',
            name='file_path',
        ),
        migrations.AddField(
            model_name='jreturns',
            name='file',
            field=models.FileField(blank=True, default='placeholder', upload_to='google/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='jreturns',
            name='photo_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, default='placeholder', upload_to='photos/%Y/%m/%d/'),
        ),
    ]