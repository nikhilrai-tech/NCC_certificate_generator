# Generated by Django 4.2.13 on 2024-07-02 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_campdetail_studentdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdetail',
            name='attach_photo_b_certificate',
            field=models.ImageField(blank=True, null=True, upload_to='static/certificates/'),
        ),
    ]
