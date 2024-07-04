# Generated by Django 4.2.13 on 2024-07-04 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CampDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_name', models.CharField(max_length=255)),
                ('date_month_year', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=100, null=True)),
                ('DOB', models.DateField(blank=True, null=True)),
                ('Guardian', models.CharField(blank=True, max_length=100, null=True)),
                ('CertificateType', models.CharField(blank=True, max_length=20, null=True)),
                ('CadetRank', models.CharField(blank=True, max_length=20, null=True)),
                ('PassingYear', models.IntegerField(blank=True, null=True)),
                ('Grade', models.CharField(blank=True, max_length=10, null=True)),
                ('Unit', models.CharField(blank=True, max_length=50, null=True)),
                ('Directorate', models.CharField(blank=True, max_length=50, null=True)),
                ('Place', models.CharField(blank=True, max_length=100, null=True)),
                ('Institute', models.CharField(blank=True, max_length=100, null=True)),
                ('certificate_number', models.CharField(blank=True, max_length=50, null=True)),
                ('serial_number', models.CharField(blank=True, max_length=50, null=True)),
                ('user_image', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('qr_code', models.ImageField(blank=True, upload_to='qr_codes/')),
                ('final_certificate', models.ImageField(blank=True, null=True, upload_to='media/certificates/')),
            ],
        ),
        migrations.CreateModel(
            name='StudentDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=255)),
                ('cbse_no', models.CharField(max_length=255)),
                ('rank', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('dob', models.DateField()),
                ('fathers_name', models.CharField(max_length=255)),
                ('school_college', models.CharField(max_length=255)),
                ('year_of_passing_b_certificate', models.CharField(max_length=255)),
                ('attach_photo_b_certificate', models.ImageField(blank=True, null=True, upload_to='media')),
                ('fresh_or_failure', models.CharField(max_length=255)),
                ('attendance_1st_year', models.IntegerField()),
                ('attendance_2nd_year', models.IntegerField()),
                ('attendance_3rd_year', models.IntegerField()),
                ('attendance_total', models.IntegerField()),
                ('home_address', models.TextField()),
                ('pass_fail', models.CharField(choices=[('Pass', 'Pass'), ('Fail', 'Fail')], max_length=10)),
                ('marks_subject1', models.IntegerField(blank=True, null=True)),
                ('marks_subject2', models.IntegerField(blank=True, null=True)),
                ('marks_subject3', models.IntegerField(blank=True, null=True)),
                ('certificate', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.certificate')),
            ],
        ),
    ]
