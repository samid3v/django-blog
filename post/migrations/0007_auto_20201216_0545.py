# Generated by Django 3.1.4 on 2020-12-16 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_auto_20201216_0538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_image',
            field=models.ImageField(blank=True, null=True, upload_to='post_image/'),
        ),
    ]
