from django.db import models



class CampDetail(models.Model):
    no_name = models.CharField(max_length=255)
    date_month_year = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

# class StudentDetail(models.Model):
#     unit = models.CharField(max_length=255)
#     cbse_no = models.CharField(max_length=255)
#     rank = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     dob = models.DateField()
#     fathers_name = models.CharField(max_length=255)
#     school_college = models.CharField(max_length=255)
#     year_of_passing_b_certificate = models.CharField(max_length=255)
#     attach_photo_b_certificate = models.ImageField(upload_to='static/certificates/', blank=True, null=True)
#     fresh_or_failure = models.CharField(max_length=255)
#     attendance_1st_year = models.IntegerField()
#     attendance_2nd_year = models.IntegerField()
#     attendance_3rd_year = models.IntegerField()
#     attendance_total = models.IntegerField()
#     home_address = models.TextField()
#     camp_details = models.ManyToManyField(CampDetail, related_name='student_details')

#     def __str__(self):
#         return self.name
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
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

    reviewer_ceo = models.ForeignKey('auth.User', related_name='ceo_reviews', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer_register_head = models.ForeignKey('auth.User', related_name='register_head_reviews', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer_staff = models.ForeignKey('auth.User', related_name='staff_reviews', on_delete=models.SET_NULL, null=True, blank=True)
    
    ceo_review_status = models.BooleanField(null=True, blank=True)
    register_head_review_status = models.BooleanField(null=True, blank=True)
    staff_review_status = models.BooleanField(null=True, blank=True)
    signature_image = models.ImageField(upload_to='signatures/', null=True, blank=True)

    def __str__(self):
        return self.Name

    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.generate_numbers()
        super().save(*args, **kwargs)

    def generate_numbers(self):
        if self.CertificateType:
            print(f"CertificateType before splitting: {self.CertificateType}")  # Add this line for debugging
            cert_type_split = self.CertificateType.split('_')
            print(f"Split result: {cert_type_split}")  # Add this line for debugging

            if len(cert_type_split) != 2:
                raise ValueError("CertificateType should be in format 'Type_Branch'")
            
            cert_type, cert_branch = cert_type_split
            prefix = f"UP/{cert_type[0]} Cert/{cert_branch}/{timezone.now().year}"
            
            last_certificate = Certificate.objects.filter(CertificateType=self.CertificateType).order_by('-serial_number').first()
            
            if last_certificate and last_certificate.serial_number:
                last_serial_number = last_certificate.serial_number.split('/')[-1]
                serial_parts = last_serial_number.split('-')
                new_serial_number = int(serial_parts[-1], 16) + 1
            else:
                new_serial_number = 1

            self.certificate_number = f"{prefix}/{new_serial_number:03}"
            self.serial_number = f"{prefix}/{new_serial_number:03}"
        else:
            raise ValueError("CertificateType must be set before generating numbers")
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