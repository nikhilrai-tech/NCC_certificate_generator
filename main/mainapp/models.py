from django.db import models

class Certificate(models.Model):
    Name = models.CharField(max_length=100)
    DOB = models.DateField()
    Guardian = models.CharField(max_length=100)
    CertificateType = models.CharField(max_length=20)
    CadetRank = models.CharField(max_length=20)
    PassingYear = models.IntegerField()
    Grade = models.CharField(max_length=10)
    Unit = models.CharField(max_length=50)
    Directorate = models.CharField(max_length=50)
    Place = models.CharField(max_length=100)
    Institute = models.CharField(max_length=100)
    certificate_number = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50)
    user_image = models.ImageField(upload_to='media/', null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    final_certificate = models.ImageField(upload_to='media/certificates/', null=True, blank=True)
    def __str__(self):
        return self.Name

class CampDetail(models.Model):
    no_name = models.CharField(max_length=255)
    date_month_year = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

class StudentDetail(models.Model):
    unit = models.CharField(max_length=255)
    cbse_no = models.CharField(max_length=255)
    rank = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    fathers_name = models.CharField(max_length=255)
    school_college = models.CharField(max_length=255)
    year_of_passing_b_certificate = models.CharField(max_length=255)
    attach_photo_b_certificate = models.ImageField(upload_to='static/certificates/', blank=True, null=True)
    fresh_or_failure = models.CharField(max_length=255)
    attendance_1st_year = models.IntegerField()
    attendance_2nd_year = models.IntegerField()
    attendance_3rd_year = models.IntegerField()
    attendance_total = models.IntegerField()
    home_address = models.TextField()
    camp_details = models.ManyToManyField(CampDetail, related_name='student_details')

    def __str__(self):
        return self.name
