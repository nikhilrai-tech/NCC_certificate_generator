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