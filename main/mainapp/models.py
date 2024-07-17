from django.db import models



class CampDetail(models.Model):
    no_name = models.CharField(max_length=255)
    date_month_year = models.CharField(max_length=255)
    location = models.CharField(max_length=255)


from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from PIL import Image
import io
import os
import logging
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
logger = logging.getLogger(__name__)
class CertificateNumberConfig(models.Model):
    CERTIFICATE_TYPE_CHOICES = [
        ('A_Army', 'A Army'),
        ('A_AirForce', 'A AirForce'),
        ('A_Navy', 'A Navy'),
        ('B_AirForce', 'B AirForce'),
        ('B_Army', 'B Army'),
        ('B_Navy', 'B Navy'),
        ('C_Army', 'C Army'),
    ]
    certificate_type = models.CharField(max_length=20, choices=CERTIFICATE_TYPE_CHOICES, unique=True)
    starting_number = models.PositiveIntegerField()
    ending_number = models.PositiveIntegerField()
    current_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.get_certificate_type_display()} Configuration"
class Certificate(models.Model):
    CERTIFICATE_TYPE_CHOICES = [
        ('A_Army', 'A Army'),
        ('A_AirForce', 'A AirForce'),
        ('A_Navy', 'A Navy'),
        ('B_AirForce', 'B AirForce'),
        ('B_Army', 'B Army'),
        ('B_Navy', 'B Navy'),
        ('C_Army', 'C Army'),
    ]

    Name = models.CharField(max_length=100, null=True, blank=True)
    DOB = models.DateField(null=True, blank=True)
    Guardian = models.CharField(max_length=100, null=True, blank=True)
    CertificateType = models.CharField(max_length=20, choices=CERTIFICATE_TYPE_CHOICES, null=True, blank=True)
    CadetRank = models.CharField(max_length=20, null=True, blank=True)
    PassingYear = models.IntegerField(null=True, blank=True)
    Grade = models.CharField(max_length=10, null=True, blank=True)
    Unit = models.CharField(max_length=50, null=True, blank=True)
    Directorate = models.CharField(max_length=50, null=True, blank=True)
    Place = models.CharField(max_length=100, null=True, blank=True)
    Institute = models.CharField(max_length=100, null=True, blank=True)
    certificate_number = models.CharField(max_length=50, null=True, blank=True)
    serial_number = models.CharField(max_length=50, null=True, blank=True)
    user_image = models.ImageField(upload_to='media/', null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    final_certificate = models.ImageField(upload_to='media/certificates/', null=True, blank=True)
    is_duplicate = models.BooleanField(default=False)
    reviewer_ceo = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ceo_reviews', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer_register_head = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='register_head_reviews', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer_staff = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='staff_reviews', on_delete=models.SET_NULL, null=True, blank=True)
    ceo_review_status = models.BooleanField(null=True, blank=True)
    register_head_review_status = models.BooleanField(null=True, blank=True)
    staff_review_status = models.BooleanField(null=True, blank=True)
    signature_image = models.ImageField(upload_to='signatures/', null=True, blank=True)
    is_signed = models.BooleanField(default=False)
    issue_date = models.DateField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)

    def formatted_issue_date(self):
        return self.issue_date.strftime('%d/%m/%Y')


    def __str__(self):
        return self.Name

    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.generate_numbers()
        super().save(*args, **kwargs)

    def generate_numbers(self):
        if not self.CertificateType:
            raise ValueError("CertificateType must be set before generating numbers")
        
        cert_type = self.CertificateType
        
        # Debugging statement
        print(f"Generating numbers for CertificateType: {cert_type}")

        # Fetch the configuration for the current certificate type
        try:
            config = CertificateNumberConfig.objects.get(certificate_type=cert_type)
        except CertificateNumberConfig.DoesNotExist:
            raise ValidationError(f"Configuration for CertificateType {cert_type} does not exist")

        if config.current_number < config.starting_number:
            config.current_number = config.starting_number
        elif config.current_number >= config.ending_number:
            raise ValidationError(f"Certificate numbers for {cert_type} type have reached the ending number")

        new_serial_number = config.current_number + 1
        config.current_number = new_serial_number
        config.save()

        cert_type_split = cert_type.split('_')
        cert_type_initial = cert_type_split[0][0]
        cert_branch_initial = cert_type_split[1][0]

        self.serial_number = f"UP{timezone.now().year}{cert_type_initial}{cert_branch_initial}A{new_serial_number:06}"
        self.certificate_number = f"UP/{cert_type_initial} Cert/{cert_type_split[1]}/{timezone.now().year}/{new_serial_number:01}"

    def apply_signature(self, role, signature_file):
        logger.debug(f"Applying signature for role: {role}, Certificate ID: {self.id}, Signature file: {signature_file}")
        if self.final_certificate and signature_file:
            try:
                with Image.open(self.final_certificate.path) as base_image:
                    with Image.open(signature_file) as signature:
                        signature = signature.convert("RGBA")
                        
                        # Determine the position based on CertificateType
                        if self.CertificateType == 'C_Army':
                            position = (684, 1416)  # Adjust the position for C_Army
                        else:
                            position = (1372, 2409)  # Default position for other types

                        # Paste signature onto certificate
                        base_image.paste(signature, position, signature)
                        
                        # Save modified image back to final_certificate
                        buffer = io.BytesIO()
                        base_image.save(buffer, format='PNG')
                        self.final_certificate.save(f"{self.Name}_signed.png", ContentFile(buffer.getvalue()))
                        
                        # Update is_signed status
                        self.is_signed = True
                        self.save()
                        logger.debug(f"Signature successfully applied to Certificate {self.id}")
            except Exception as e:
                logger.error(f"Error applying signature to Certificate {self.id}: {e}")

    # def generate_numbers(self):
    #     if self.CertificateType:
    #         cert_type_split = self.CertificateType.split('_')

    #         if len(cert_type_split) != 2:
    #             raise ValueError("CertificateType should be in format 'Type_Branch'")
            
    #         cert_type, cert_branch = cert_type_split
    #         prefix = f"UP{timezone.now().year}{cert_type[0]}{cert_branch[0]}A"  # Adjust the prefix as needed
            
    #         # Find the last serial number for the given CertificateType
    #         last_certificate = Certificate.objects.filter(CertificateType=self.CertificateType).order_by('-id').first()
            
    #         if last_certificate and last_certificate.serial_number:
    #             # Extract the numeric part from serial_number
    #             last_serial_number = last_certificate.serial_number.split('/')[-1].split('A')[-1]
    #             new_serial_number = int(last_serial_number) + 1
    #         else:
    #             new_serial_number = 1

    #         # Format new serial number for serial_number
    #         self.serial_number = f"UP{timezone.now().year}{cert_type[0]}{cert_branch[0]}A{new_serial_number:06}"
            
    #         # For certificate_number, keep the existing format
    #         self.certificate_number = f"UP/{cert_type[0]} Cert/{cert_branch}/{timezone.now().year}/{new_serial_number:03}"
    #     else:
    #         raise ValueError("CertificateType must be set before generating numbers")
        




class StudentDetail(models.Model):
    unit = models.CharField(max_length=255)
    cbse_no = models.CharField(max_length=255)
    rank = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    certificate = models.OneToOneField(Certificate, on_delete=models.CASCADE, null=True, blank=True)
    fathers_name = models.CharField(max_length=255)
    school_college = models.CharField(max_length=255)
    year_of_passing_b_certificate = models.CharField(max_length=255)
    attach_photo_b_certificate = models.ImageField(upload_to='media', blank=True, null=True)
    fresh_or_failure = models.CharField(max_length=255)
    attendance_1st_year = models.IntegerField()
    attendance_2nd_year = models.IntegerField()
    attendance_3rd_year = models.IntegerField()
    attendance_total = models.IntegerField()
    # admit_card_path = models.CharField(max_length=255, blank=True, null=True)
    home_address = models.TextField()
    pass_fail = models.CharField(max_length=10, choices=[('Pass', 'Pass'), ('Fail', 'Fail')])
    marks_subject1 = models.IntegerField(blank=True, null=True)
    marks_subject2 = models.IntegerField(blank=True, null=True)
    marks_subject3 = models.IntegerField(blank=True, null=True)
    camp_name = models.CharField(max_length=255)  # New field
    camp_date_from = models.DateField()  # New field
    camp_date_to = models.DateField()  # New field
    camp_location = models.CharField(max_length=255)  # New field


class HelpRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    request_type = models.CharField(max_length=50, choices=[('CEO', 'CEO'), ('Staff', 'Staff'), ('Colonel', 'Colonel'),('Cyber3ra Support', 'Cyber3ra Support')])
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Help request from {self.name} to {self.request_type}"

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username