# Generated by Django 4.1.1 on 2022-10-02 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, default='/images/placeholder.png', null=True, upload_to='images'),
        ),
    ]
