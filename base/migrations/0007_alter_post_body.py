# Generated by Django 4.1.1 on 2022-10-03 12:09

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0006_post_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="body",
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
