# Generated by Django 4.2.13 on 2024-07-24 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_certificate_ceo_signature_applied_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='preview_image',
            field=models.ImageField(blank=True, null=True, upload_to='certificate_previews/'),
        ),
    ]
