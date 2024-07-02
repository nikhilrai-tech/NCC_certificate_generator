"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainapp . views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generate/', generate_certificate, name='generate_certificate'),
    path('view-certificates/', view_certificates, name='view_certificates'),
    path('view-certificate/<int:certificate_id>/', view_certificate_detail, name='view_certificate_detail'),
    path('download-all-certificates/', download_all_certificates, name='download_all_certificates'),
    path('certificate/<int:certificate_id>/download/',download_certificate_detail, name='download_certificate_detail'),
    path('certificate-success/', certificate_success, name='certificate_success'),
    path('qr_scan/<int:certificate_id>/',qr_scan_view, name='qr_scan'),
    path('login/', custom_login, name='custom_login'),
    path('staff/', register_staff, name='register_staff'),
    path('clerk/', register_clerk, name='register_clerk'),
    path('head/', register_head, name='register_head'),
    path('ceo/', register_ceo, name='register_ceo'),
    path('', home, name='home'),
    path('signuppage/',signuppage, name='signuppage'),
    path('forgotpass/',forgotpass, name='forgotpass'),
    path('dashboard/',dashboard, name='dashboard'),
    path('main/',mintemplate, name='main'),
    path('admincard/',admincard, name='admincard'),
    path('student/', student_detail_view, name='student_detail'),
    path('success/', success_view, name='success'),
    path('admit/', student_detail_basic_view, name='student_detail_basic'),
    path('extended/<int:student_id>/', student_detail_extended_view, name='student_detail_extended'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)