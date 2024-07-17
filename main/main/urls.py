from django.contrib import admin
from django.urls import path,include
from mainapp . views import *
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generate/', generate_certificate, name='generate_certificate'),
    path('view-certificates/', view_certificates, name='view_certificates'),
    path('view-certificate/<int:certificate_id>/', view_certificate_detail, name='view_certificate_detail'),
    path('download-all-certificates/', download_all_certificates, name='download_all_certificates'),
    path('certificate/<int:certificate_id>/download/',download_certificate_detail, name='download_certificate_detail'),
    path('certificate-success1/', certificate_success1, name='certificate_success'),
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
    path('success2/', success_view2, name='success'),
    path('admit/', student_detail_basic_view, name='student_detail_basic'),
    path('extended/<int:student_id>/', student_detail_extended_view, name='student_detail_extended'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
    path('cert/', certhome, name='cert'),
    path('edit/<int:id>/', edit_student_detail, name='edit_student_detail'),
    path('success/', certificate_success, name='certificate_success1'),
    path('forgotpass/', forgotpass, name='forgotpass'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', logout_view, name='logout'),
    path('update_user/', update_user, name='update_user'),
    path('verify_certificate/<int:certificate_id>/', verify_certificate_view, name='verify_certificate_view'),
    path('generate_duplicate_certificate/', generate_duplicate_certificate, name='generate_duplicate_certificate'),
    path('download_duplicate_certificate/', download_duplicate_certificate, name='download_duplicate_certificate'),
    path('rejected_certificates/register_head/', rejected_certificates_register_head, name='rejected_certificates_register_head'),
    path('rejected_certificates/ceo/', rejected_certificates_ceo, name='rejected_certificates_ceo'),
    path('rejected_certificates/staff/', rejected_certificates_staff, name='rejected_certificates_staff'),
    path('signed_certificates/', signed_certificates_view, name='signed_certificates'),
    path('signed_certificatestrue/', signed_certificates_viewtrue, name='signed_certificatestrue'),
    path('unsigned-certificates/', unsigned_certificates_view, name='unsigned_certificates'),
    # path('view_admit_card/<int:student_id>/', view_admit_card, name='view_admit_card'),
    # path('view_admit_card/<int:student_id>/', view_admit_card, name='view_admit_card'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)