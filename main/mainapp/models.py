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
class Certificate(models.Model):
    CERTIFICATE_TYPE_CHOICES = [
        ('A_Army', 'A Army'),
        ('A_AirForce', 'A AirForce'),
        ('A_Navy', 'A Navy'),
        ('B_AirForce', 'B AirForce'),
        ('B_Army', 'B Army'),
        ('B_Navy', 'B Navy'),
        ('C', 'C'),
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

    def __str__(self):
        return self.Name
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