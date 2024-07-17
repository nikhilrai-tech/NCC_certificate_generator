from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(StudentDetail)
admin.site.register(CampDetail)

# @admin.register(Certificate)
# class certificateadmin(admin.ModelAdmin):
#     list_display=["DOB"]


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('Name', 'CertificateType', 'certificate_number', 'serial_number')
    search_fields = ('Name', 'CertificateType', 'certificate_number', 'serial_number')
    list_filter = ('CertificateType', 'PassingYear')

@admin.register(CertificateNumberConfig)
class CertificateNumberConfigAdmin(admin.ModelAdmin):
    list_display = ('certificate_type', 'starting_number', 'ending_number', 'current_number')
