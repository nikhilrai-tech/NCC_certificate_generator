from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.core.files import File
from django.http import JsonResponse
from .forms import CertificateForm
from .models import Certificate
from io import BytesIO
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings
from .forms import StudentDetailForm, CampDetailForm, HelpForm,CustomPasswordResetForm
from .models import CampDetail
from django.core.mail import send_mail
def generate_certificate(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            certificate = form.save()  # Save form data and commit to database to get the ID

            # Generate QR code with certificate URL
            qr_url = request.build_absolute_uri(f"/qr_scan/{certificate.id}/")
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_url)
            qr.make(fit=True)

            # Create QR code image
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Save QR code image to memory buffer
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')  # Save as PNG format
            buffer.seek(0)

            # Save QR code image to the model instance's qr_code field
            certificate.qr_code.save(f'{certificate.Name}_qr.png', File(buffer))

            # Select the appropriate JPG template based on the certificate type
            jpg_template_path = os.path.join(settings.BASE_DIR, f"templates/certificates/{certificate.CertificateType}.jpg")
            certificate_img = Image.open(jpg_template_path)

            # Overlay QR code onto the certificate image
            qr_img = qr_img.resize((100, 100))  # Adjust the size as needed
            certificate_img.paste(qr_img, (50, 50))  # Adjust the position as needed

            # Draw text on the certificate image
            draw = ImageDraw.Draw(certificate_img)
            font_path = os.path.join(settings.BASE_DIR, "arial.ttf")  # Path to a TTF font file
            font = ImageFont.truetype(font_path, 60)  # Adjust the font size as needed

            # Define positions for the text fields
            text_positions = {
                # 'ID': (200, 50),
                'Name': ((436,1353)),
                'DOB': (200, 110),
                'Guardian': (200, 140),
                'CertificateType': (200, 170),
                'CadetRank': (200, 200),
                'PassingYear': (200, 230),
                'Grade': (200, 260),
                'Unit': (200, 290),
                'Directorate': (200, 320),
                'Place': (200, 350),
                'Institute': (200, 380),
                'CertificateNumber': (200, 410),
                'SerialNumber': (200, 440),
            }

            # Draw each field on the certificate image
            # draw.text(text_positions['ID'], f"ID: {certificate.ID}", font=font, fill="black")
            draw.text(text_positions['Name'], f" {certificate.Name}", font=font, fill="black")
            draw.text(text_positions['DOB'], f"DOB: {certificate.DOB}", font=font, fill="black")
            draw.text(text_positions['Guardian'], f"Guardian: {certificate.Guardian}", font=font, fill="black")
            draw.text(text_positions['CertificateType'], f"Certificate Type: {certificate.CertificateType}", font=font, fill="black")
            draw.text(text_positions['CadetRank'], f"Cadet Rank: {certificate.CadetRank}", font=font, fill="black")
            draw.text(text_positions['PassingYear'], f"Passing Year: {certificate.PassingYear}", font=font, fill="black")
            draw.text(text_positions['Grade'], f"Grade: {certificate.Grade}", font=font, fill="black")
            draw.text(text_positions['Unit'], f"Unit: {certificate.Unit}", font=font, fill="black")
            draw.text(text_positions['Directorate'], f"Directorate: {certificate.Directorate}", font=font, fill="black")
            draw.text(text_positions['Place'], f"Place: {certificate.Place}", font=font, fill="black")
            draw.text(text_positions['Institute'], f"Institute: {certificate.Institute}", font=font, fill="black")
            draw.text(text_positions['CertificateNumber'], f"Certificate Number: {certificate.certificate_number}", font=font, fill="black")
            draw.text(text_positions['SerialNumber'], f"Serial Number: {certificate.serial_number}", font=font, fill="black")

            if certificate.user_image:
                    user_img = Image.open(certificate.user_image.path)
                    user_img = user_img.resize((100, 100))  # Adjust the size as needed
                    certificate_img.paste(user_img, (300, 50)) 
            # Save the final certificate image to memory buffer
            final_buffer = BytesIO()
            certificate_img.save(final_buffer, format='JPEG')
            final_buffer.seek(0)

            # Save the final certificate image to the model instance's final_certificate field
            certificate.final_certificate.save(f'{certificate.Name}_certificate.jpg', File(final_buffer))

            # Save the complete form data
            certificate.save()

            return redirect('certificate_success')  # Redirect to success page after saving
    else:
        form = CertificateForm()

    return render(request, 'certificate_form.html', {'form': form})
from django.template.loader import get_template
def view_certificates(request):
    certificates = Certificate.objects.all()
    return render(request, 'view_certificates.html', {'certificates': certificates})

def view_certificate_detail(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    
    # Ensure final_certificate exists and is not None
    if certificate.final_certificate:
        with open(certificate.final_certificate.path, 'rb') as f:
            certificate_content = f.read()

        response = HttpResponse(certificate_content, content_type='image/jpeg')  # Adjust content_type based on your image type
        return response
    else:
        return HttpResponse('Certificate not found', status=404)

def download_certificate_detail(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    
    # Ensure final_certificate exists and is not None
    if certificate.final_certificate:
        with open(certificate.final_certificate.path, 'rb') as f:
            certificate_content = f.read()

        response = HttpResponse(certificate_content, content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="certificate_{certificate.id}.jpg"'
        return response
    else:
        return HttpResponse('Certificate not found', status=404)
    
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Certificate
from PIL import Image
def download_all_certificates(request):
  certificates = Certificate.objects.all()
  if not certificates:
      raise Http404("No certificates found.")

  buffer = BytesIO()
  zip_file = zipfile.ZipFile(buffer, 'w')

  for certificate in certificates:
      if certificate.final_certificate:
          file_path = certificate.final_certificate.path
          file_name = certificate.final_certificate.name
          zip_file.write(file_path, file_name)

  zip_file.close()
  buffer.seek(0)

  response = HttpResponse(buffer, content_type='application/zip')
  response['Content-Disposition'] = 'attachment; filename="all_certificates.zip"'
  return response

def certificate_success1(request):
    return render(request, 'certificate_success.html')
from django.shortcuts import render, get_object_or_404
def qr_scan_view(request, certificate_id):
    # Retrieve Certificate object based on certificate_id
    certificate = get_object_or_404(Certificate, pk=certificate_id)
    
    # Render a template with certificate information
    return render(request, 'qr_scan_popup.html', {'certificate': certificate})
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import StaffSignUpForm, ClerkSignUpForm, CEOSignUpForm, headSignUpForm

def register_staff(request):
    if request.method == 'POST':
        form = StaffSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            staff_group = Group.objects.get(name='Staff')
            staff_group.user_set.add(user)
            login(request, user)
            return redirect('custom_login')
        else:
            # Capture form errors and display them
            return render(request, 'signup_form.html', {'form': form, 'role': 'Group Commander', 'errors': form.errors})
    else:
        form = StaffSignUpForm()
    return render(request, 'signup_form.html', {'form': form, 'role': 'Group Commander'})

def register_clerk(request):
    if request.method == 'POST':
        form = ClerkSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            clerk_group = Group.objects.get(name='Clerk')
            clerk_group.user_set.add(user)
            login(request, user)
            return redirect('custom_login')
        else:
            # Capture form errors and display them
            return render(request, 'signupclerk_form.html', {'form': form, 'role': 'Clerk', 'errors': form.errors})
    else:
        form = ClerkSignUpForm()
    return render(request, 'signupclerk_form.html', {'form': form, 'role': 'Clerk'})

def register_ceo(request):
    if request.method == 'POST':
        form = CEOSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            CEO_group = Group.objects.get(name='CEO')
            CEO_group.user_set.add(user)
            login(request, user)
            return redirect('custom_login')
        else:
            # Capture form errors and display them
            return render(request, 'signupceo_form.html', {'form': form, 'role': 'CO', 'errors': form.errors})
    else:
        form = CEOSignUpForm()
    return render(request, 'signupceo_form.html', {'form': form, 'role': 'CO'})


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on user group
            if user.is_superuser:
                return redirect('/admin/')
            elif user.groups.filter(name='Staff').exists():
                return redirect('dashboard')
            elif user.groups.filter(name='Clerk').exists():
                return redirect('dashboard')
            elif user.groups.filter(name='CEO').exists():
                return redirect('dashboard')
            elif user.groups.filter(name='register_head').exists():
                return redirect('dashboard')
        else:
            return HttpResponse('Invalid login credentials')
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def signuppage(request):
    return render(request, 'signuppage.html')

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from .forms import CustomPasswordResetForm

def forgotpass(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='password_reset_email.html'
            )
            return redirect('password_reset_done')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'forgotpass.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    form_class = CustomPasswordResetForm

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


def register_head(request):
    # if request.method == 'POST':
    #     form = headSignUpForm(request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         register_head = Group.objects.get(name='register_head')
    #         register_head.user_set.add(user)
    #         login(request, user)
    #         return redirect('custom_login')
    # else:
    #     form = headSignUpForm()
    # return render(request, 'signup_form.html', {'form': form, 'role': 'state head'})
    if request.method == 'POST':
        form = headSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            register_head = Group.objects.get(name='register_head')
            register_head.user_set.add(user)
            login(request, user)
            return redirect('custom_login')
        else:
            # Capture form errors and display them
            return render(request, 'signuphead_form.html', {'form': form, 'role': 'ADG', 'errors': form.errors})
    else:
        form = headSignUpForm()
    return render(request, 'signuphead_form.html', {'form': form, 'role': 'ADG'})




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count
from .forms import HelpForm
from .models import HelpRequest, Certificate
# @login_required
@login_required
def dashboard(request):
    form = HelpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        request_type = form.cleaned_data['request_type']

        # Define recipients based on request_type
        if request_type == 'CEO':
            recipient = 'nrai91088@gmail.com'
        elif request_type == 'Staff':
            recipient = 'kanakchauhan085@gmail.com'
        elif request_type == 'Colonel':
            recipient = 'kanakchauhan.142400@gmail.com'
        elif request_type == 'Cyber3ra Support':
            recipient = 'info@cyber3ra.com'
        
        # Save the form submission to the database
        help_request = HelpRequest(
            name=name,
            email=email,
            message=message,
            request_type=request_type
        )
        help_request.save()

        # Send the email
        subject = f"Help Request to {request_type}"
        email_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        send_mail(subject, email_message, 'your_email@gmail.com', [recipient])
        form = HelpForm()

    certificate_data = Certificate.objects.values('CertificateType').annotate(count=Count('CertificateType')).order_by('CertificateType')
    total_certificates = Certificate.objects.count()
    pending_ceo_approval = Certificate.objects.filter(ceo_review_status=False).count()
    pending_register_head_approval = Certificate.objects.filter(register_head_review_status=False).count()
    pending_staff_approval = Certificate.objects.filter(staff_review_status=False).count()

    # Get pending approvals per user
    reviewers_ceo = User.objects.filter(ceo_reviews__ceo_review_status=False).distinct()
    reviewers_register_head = User.objects.filter(register_head_reviews__register_head_review_status=False).distinct()
    reviewers_staff = User.objects.filter(staff_reviews__staff_review_status=False).distinct()

    reviewers_ceo_pending = {reviewer.username: reviewer.ceo_reviews.filter(ceo_review_status=False).count() for reviewer in reviewers_ceo}
    reviewers_register_head_pending = {reviewer.username: reviewer.register_head_reviews.filter(register_head_review_status=False).count() for reviewer in reviewers_register_head}
    reviewers_staff_pending = {reviewer.username: reviewer.staff_reviews.filter(staff_review_status=False).count() for reviewer in reviewers_staff}
    
    # Filter certificates based on user's group
    user = request.user
    group_name = None
    if user.groups.filter(name='CEO').exists():
        group_name = 'CEO'
        certificates = Certificate.objects.filter(CertificateType__in=['A_Army', 'A_AirForce', 'A_Navy', 'B_Army', 'B_AirForce', 'B_Navy', 'C_Army'])
    elif user.groups.filter(name='Staff').exists():
        group_name = 'Staff'
        certificates = Certificate.objects.filter(CertificateType__in=['B_Army', 'B_AirForce', 'B_Navy', 'C_Army'])
    elif user.groups.filter(name='register_head').exists():
        group_name = 'register_head'
        certificates = Certificate.objects.filter(CertificateType='C_Army')
    else:
        certificates = Certificate.objects.all()
    
    pass_count = StudentDetail.objects.filter(pass_fail='Pass').count()
    fail_count = StudentDetail.objects.filter(pass_fail='Fail').count()
    is_clerk = request.user.groups.filter(name='Clerk').exists()
    students = StudentDetail.objects.all()

    labels = []
    data = []
    for item in certificate_data:
        cert_type = item['CertificateType']
        if cert_type:
            labels.append(dict(Certificate.CERTIFICATE_TYPE_CHOICES).get(cert_type, cert_type))
            data.append(item['count'])

    context = {
        'form': form,
        'labels': labels,
        'data': data,
        'total_certificates': total_certificates,
        'pending_ceo_approval': pending_ceo_approval,
        'pending_register_head_approval': pending_register_head_approval,
        'pending_staff_approval': pending_staff_approval,
        'reviewers_ceo_pending': reviewers_ceo_pending,
        'reviewers_register_head_pending': reviewers_register_head_pending,
        'reviewers_staff_pending': reviewers_staff_pending,
        'pass_count': pass_count,
        'fail_count': fail_count,
        'is_clerk': is_clerk,
        'certificates': certificates,
        'students': students
    }

    return render(request, "dashboard.html", context)

def mintemplate(request):
    certificates = Certificate.objects.all()
    user = request.user

    # Determine the user's group
    is_ceo = user.groups.filter(name='CEO').exists()
    is_staff = user.groups.filter(name='Staff').exists()
    is_clerk = user.groups.filter(name='Clerk').exists()
    is_register_head = user.groups.filter(name='register_head').exists()


    # Filter certificates based on the user's group
    if is_ceo:
        certificates = certificates.filter(CertificateType__in=['A_Army', 'A_AirForce', 'A_Navy','B_Army', 'B_AirForce', 'B_Navy','C_Army'])
    elif is_staff:
        certificates = certificates.filter(CertificateType__in=['B_Army', 'B_AirForce', 'B_Navy','C_Army'])
    elif is_register_head:
        certificates = certificates.filter(CertificateType__in=['C_Army'])

    return render(request, "maintemp.html", {'certificates': certificates, 'is_clerk': is_clerk})



def admincard(request):
    return render(request,"admincard.html")


from .forms import StudentDetailForm, CampDetailForm
from django.shortcuts import render, redirect
from .forms import StudentDetailForm, CampDetailForm
from .models import StudentDetail, CampDetail

def student_detail_view(request):
    if request.method == 'POST':
        student_form = StudentDetailForm(request.POST, request.FILES)
        camp_forms = []
        camp_data = []

        for i in range(len(request.POST.getlist('camp_no_name[]'))):
            camp_form = CampDetailForm({
                'no_name': request.POST.getlist('camp_no_name[]')[i],
                'date_month_year': request.POST.getlist('camp_date_month_year[]')[i],
                'location': request.POST.getlist('camp_location[]')[i],
            })
            camp_forms.append(camp_form)
            if camp_form.is_valid():
                camp_data.append(camp_form.save())

        if student_form.is_valid() and all([cf.is_valid() for cf in camp_forms]):
            student = student_form.save(commit=False)
            student.save()
            student.camp_details.set(camp_data)
            student.save()
            return render(request, 'success.html')  # Replace 'success.html' with your success template

    else:
        student_form = StudentDetailForm()
        empty_camp_form = CampDetailForm()

    context = {
        'student_form': student_form,
        'empty_camp_form': empty_camp_form,
    }

    return render(request, 'admincard.html', context)

# def student_detail_view(request):
#     student_form = StudentDetailForm()
#     return render(request, 'admincard.html', {"student_form": student_form})

def student_detail_view(request):
    if request.method == 'POST':
        form = StudentDetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = StudentDetailForm()
    return render(request, 'student_detail_form.html', {'form': form})

def success_view2(request):
    students = StudentDetail.objects.all()
    return render(request, 'success copy.html', {'students': students})

from django.shortcuts import render, get_object_or_404
def student_detail_single_view(request, student_id):
    student = get_object_or_404(StudentDetail, id=student_id)
    return render(request, 'student_detail_single.html', {'student': student})
from .forms import StudentDetailExtendedForm,StudentDetailBasicForm

def student_detail_basic_view(request):
    if request.method == 'POST':
        form = StudentDetailBasicForm(request.POST, request.FILES)
        if form.is_valid():
            student_detail = form.save()
            if student_detail.pass_fail == 'Pass' and not student_detail.certificate:
                certificate = Certificate.objects.create(
                    Name=student_detail.name,
                    DOB=student_detail.dob,
                    Guardian=student_detail.fathers_name,
                    CadetRank=student_detail.rank,
                    Unit=student_detail.unit,
                    Institute=student_detail.school_college,
                    user_image=student_detail.attach_photo_b_certificate,
                )
                student_detail.certificate = certificate
                student_detail.save()
            return redirect('success')
    else:
        form = StudentDetailBasicForm()
    return render(request, 'student_detail_basic.html', {'form': form})

def student_detail_extended_view(request, student_id):
    student = get_object_or_404(StudentDetail, id=student_id)
    
    if request.method == 'POST':
        form = StudentDetailExtendedForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            if student.pass_fail == 'Pass':
                if not student.certificate:
                    if student.unit and student.rank:
                        try:
                            # Set a default CertificateType if not provided
                            certificate_type = 'A_Army'  # You can set this based on your logic
                            
                            certificate = Certificate.objects.create(
                                Name=student.name,
                                DOB=student.dob,
                                Guardian=student.fathers_name,
                                CadetRank=student.rank,
                                CertificateType=certificate_type,
                                Unit=student.unit,
                                Institute=student.school_college,
                                user_image=student.attach_photo_b_certificate,
                            )
                            student.certificate = certificate
                            student.save()
                        except Exception as e:
                            print(e)
                            form.add_error(None, f"Error creating certificate: {str(e)}")
                else:
                    certificate = student.certificate
                    certificate.Name = student.name
                    certificate.DOB = student.dob
                    certificate.Guardian = student.fathers_name
                    certificate.CadetRank = student.rank
                    certificate.Unit = student.unit
                    certificate.Institute = student.school_college
                    certificate.user_image = student.attach_photo_b_certificate
                    certificate.save()
            else:
                if student.certificate:
                    student.certificate.delete()
                    student.certificate = None
                    student.save()
            return redirect('dashboard')
    else:
        form = StudentDetailExtendedForm(instance=student)
    
    return render(request, 'student_detail_extended.html', {'form': form})
import zipfile
import os
from io import BytesIO
from reportlab.lib.units import inch
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
# from myproject.students.models import StudentDetail  # Uncomment and adjust the import as needed

def generate_pdf(request):
    students = StudentDetail.objects.all()

    # Prepare in-memory zip file
    zip_buffer = BytesIO()
    zip_file = zipfile.ZipFile(zip_buffer, 'w')

    # Load JPG template as background
    template_path = '../main/mainapp/static/t2.jpeg'  # Replace with your template path

    for student in students:
        # Create PDF document
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)

        # Draw template background
        background_image = ImageReader(template_path)
        c.drawImage(background_image, 0, 0, width=letter[0], height=letter[1], preserveAspectRatio=True)

        # Function to draw text at specific coordinates
        def draw_text(c, x, y, text, font_size=12):
            c.setFont("Helvetica", font_size)
            c.drawString(x, y, text)

        # Adjusted coordinates for your template
        coordinates = {
            'unit': (330, 740),
            'cbse_no': (330, 695),
            'rank': (330, 675),
            'name': (330, 655),
            'dob': (330, 590),
            'fathers_name': (330, 540),
            'school_college': (330, 480),
            'year_of_passing_b_certificate': (330, 450),
            'fresh_or_failure': (330, 410),
            'attendance_total': (260, 350),
            'camp_name': (150, 275),  # Adjusted to fit within the page
            'camp_date_from': (310, 275),  # Adjusted to fit within the page
            'camp_date_to': (360, 275),  # Adjusted to fit within the page
            'camp_location': (415, 275),  # Adjusted to fit within the page
            'home_address': (330, 230),  # Adjusted to fit within the page
        }

        # Draw the text at specified coordinates
        draw_text(c, *coordinates['unit'], f"{student.unit}")
        draw_text(c, *coordinates['cbse_no'], f"{student.cbse_no}")
        draw_text(c, *coordinates['rank'], f"{student.rank}")
        draw_text(c, *coordinates['name'], f"{student.name}")

        # Format the date as dd/mm/yyyy
        formatted_dob = student.dob.strftime('%d/%m/%Y')
        draw_text(c, *coordinates['dob'], f"{formatted_dob}")

        draw_text(c, *coordinates['fathers_name'], f"{student.fathers_name}")
        draw_text(c, *coordinates['school_college'], f"{student.school_college}")
        draw_text(c, *coordinates['year_of_passing_b_certificate'], f"{student.year_of_passing_b_certificate}")
        draw_text(c, *coordinates['fresh_or_failure'], f"{student.fresh_or_failure}")
        draw_text(c, *coordinates['attendance_total'], f"{student.attendance_total}")
        draw_text(c, *coordinates['home_address'], f"{student.home_address}")
        draw_text(c, *coordinates['camp_name'], f"{student.camp_name}")
        draw_text(c, *coordinates['camp_date_from'], f"{student.camp_date_from.strftime('%d/%m/%Y') if student.camp_date_from else ''}", font_size=8)
        draw_text(c, *coordinates['camp_date_to'], f"{student.camp_date_to.strftime('%d/%m/%Y') if student.camp_date_to else ''}", font_size=8)
        draw_text(c, *coordinates['camp_location'], f"{student.camp_location}")

        # Display photo if available
        if student.attach_photo_b_certificate:
            image_path = student.attach_photo_b_certificate.path
            c.drawImage(image_path, 500, 650, width=100, height=80, preserveAspectRatio=True)

        # Save the PDF to in-memory buffer
        c.save()

        # Add PDF buffer to zip file
        zip_file.writestr(f"{student.name}_admitcard.pdf", pdf_buffer.getvalue())

    # Close the zip file
    zip_file.close()

    # Create HttpResponse with zip file content
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="admitcards.zip"'

    return response

def certhome(request):
    fm=Certificate.objects.all()
    print(fm)
    return render(request,"certhome.html",{"fm":fm})

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from django.core.files.base import ContentFile
import qrcode
from io import BytesIO
from PIL import Image
import os
from django.shortcuts import render, get_object_or_404, redirect
from .models import StudentDetail
from .forms import CertificateForm
from django.conf import settings
from PyPDF2 import PdfReader, PdfWriter

# def draw_grid(c, width, height, step=50):
#   c.setStrokeColorRGB(0.8, 0.8, 0.8)  # Light gray color for the grid
#   c.setLineWidth(0.1)  # Thinner lines
#   c.setFont("Helvetica", 5)  # Smaller font for labels

#   # Draw vertical lines
#   for x in range(0, int(width) + step, step):
#       c.line(x, 0, x, height)
#       c.drawString(x + 1, 5, str(x))  # Bottom label
#       c.drawString(x + 1, height - 10, str(x))  # Top label

#   # Draw horizontal lines
#   for y in range(0, int(height) + step, step):
#       c.line(0, y, width, y)
#       c.drawString(5, y + 1, str(y))  # Left label
#       c.drawString(width - 20, y + 1, str(y))  # Right label

def edit_student_detail(request, id):
  student_detail = get_object_or_404(StudentDetail, id=id)
  certificate = student_detail.certificate

  if request.method == 'POST':
      certificate_form = CertificateForm(request.POST, request.FILES, instance=certificate)

      if certificate_form.is_valid():
          certificate = certificate_form.save(commit=False)

          try:
              certificate.generate_numbers()
          except ValueError as e:
              print(f"Error generating numbers: {e}")
              return render(request, 'edit_student_detail.html', {
                  'certificate_form': certificate_form,
                  'student_detail': student_detail,
                  'error_message': str(e),
              })

          qr_url = request.build_absolute_uri(f"/qr_scan/{certificate.id}/")
          qr = qrcode.QRCode(
              version=1,
              error_correction=qrcode.constants.ERROR_CORRECT_L,
              box_size=10,
              border=4,
          )
          qr.add_data(qr_url)
          qr.make(fit=True)

          qr_img = qr.make_image(fill_color="black", back_color="white")

          buffer = BytesIO()
          qr_img.save(buffer, format='PNG')
          buffer.seek(0)

          certificate.qr_code.save(f'{certificate.Name}_qr.png', File(buffer))

          pdf_template_path = os.path.join(settings.BASE_DIR, f"templates/certificates/{certificate.CertificateType}.pdf")

          c_army_text_positions = {
              'Name': (100, 400),
              'DOB': (450, 360),
              'Guardian': (470, 400),
              'CadetRank': (425, 450),
              'PassingYear': (260, 195),
              'Grade': (500, 2400),
              'Unit': (100, 360),
              'Directorate': (200, 300),
              'Place': (100, 50),
              'certificate_number': (400, 780),
              'serial_number': (100, 450),
              'qr_code': (450, 660),
              'user_image': (50, 660),
              'issue_date': (90, 10),
          }

          default_text_positions = {
              'Name': (100, 520),
              'DOB': (400, 470),
              'Guardian': (450, 520),
              'CadetRank': (400, 560),
              'PassingYear': (300, 320),
              'Grade': (130, 270),
              'Unit': (100, 465),
              'Directorate': (200, 420),
              'Place': (100, 200),
              'certificate_number': (370, 760),
              'serial_number': (70, 560),
              'qr_code': (500, 660),
              'user_image': (50, 660),
              'issue_date': (100, 160),
          }

          if certificate.CertificateType == 'C_Army':
              text_positions = c_army_text_positions
              qr_img_size = (90, 90)
              user_img_size = (90, 90)
              font_size = 15
          else:
              text_positions = default_text_positions
              qr_img_size = (90, 90)
              user_img_size = (90, 90)
              font_size = 15

          qr_img = qr_img.resize(qr_img_size)

          buffer = BytesIO()
          c = canvas.Canvas(buffer, pagesize=letter)

          # Draw the grid
        #   draw_grid(c, letter[0], letter[1])

          qr_img_reader = ImageReader(qr_img)
          c.drawImage(qr_img_reader, *text_positions['qr_code'], width=qr_img_size[0], height=qr_img_size[1])

          if certificate.user_image:
              user_img = Image.open(certificate.user_image.path)
              user_img = user_img.resize(user_img_size)
              user_img_reader = ImageReader(user_img)
              c.drawImage(user_img_reader, *text_positions['user_image'], width=user_img_size[0], height=user_img_size[1])

          c.setFont("Helvetica", font_size)

          for field, pos in text_positions.items():
              if field not in ['qr_code', 'user_image'] and hasattr(certificate, field):
                  value = str(getattr(certificate, field))
                  if field == 'issue_date':
                      value = certificate.issue_date.strftime('%d/%m/%Y')
                  if field == 'DOB':
                      value = certificate.DOB.strftime('%d/%m/%Y')
                  c.drawString(pos[0], pos[1], value)

          c.save()

          buffer.seek(0)
          overlay_pdf = PdfReader(buffer)
          template_pdf = PdfReader(open(pdf_template_path, "rb"))
          output_pdf = PdfWriter()

          for page_num in range(len(template_pdf.pages)):
              template_page = template_pdf.pages[page_num]
              if page_num < len(overlay_pdf.pages):
                  overlay_page = overlay_pdf.pages[page_num]
                  template_page.merge_page(overlay_page)
              output_pdf.add_page(template_page)

          final_buffer = BytesIO()
          output_pdf.write(final_buffer)
          final_buffer.seek(0)

          certificate.final_certificate.save(f'{certificate.Name}_certificate.pdf', ContentFile(final_buffer.getvalue()))

          certificate.save()

          return redirect('dashboard')

      else:
          print("Certificate Form Errors: ", certificate_form.errors)

  else:
      certificate_form = CertificateForm(instance=certificate)

  return render(request, 'edit_student_detail.html', {
      'certificate_form': certificate_form,
      'student_detail': student_detail,
  })

def certificate_success(request):
    return render(request, 'certificate_success1.html')

from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('custom_login')

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserUpdateForm
from .models import UserProfile

@login_required
def update_user(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the profile page or another page after updating
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'update_user.html', {'form': form})

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Certificate
import logging

logger = logging.getLogger(__name__)

import logging
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Certificate
from django.conf import settings
import os

logger = logging.getLogger(__name__)

@login_required
def verify_certificate_view(request, certificate_id):
  certificate = get_object_or_404(Certificate, id=certificate_id)
  user = request.user
  can_verify = False
  group_name = None

  # Determine the user's group
  if user.groups.filter(name='CEO').exists():
      group_name = 'CEO'
  elif user.groups.filter(name='register_head').exists():
      group_name = 'register_head'
  elif user.groups.filter(name='Staff').exists():
      group_name = 'Staff'

  # Determine if the user can verify this certificate based on their group
  if certificate.CertificateType.startswith('A_'):
      can_verify = group_name == 'CEO'
  elif certificate.CertificateType.startswith('B_'):
      can_verify = group_name in ['CEO', 'Staff']
  elif certificate.CertificateType == 'C_Army':
      can_verify = group_name in ['CEO', 'register_head', 'Staff']

  if request.method == 'POST' and can_verify:
      action = request.POST.get('action')
      remarks = request.POST.get('remarks')

      if action == 'check':
          certificate.checked_by = user
      elif action == 'revise':
          certificate.revised_by = user
      elif group_name == 'CEO':
          certificate.reviewer_ceo = user
          certificate.ceo_review_status = (action == 'approve')
      elif group_name == 'register_head':
          certificate.reviewer_register_head = user
          certificate.register_head_review_status = (action == 'approve')
      elif group_name == 'Staff':
          certificate.reviewer_staff = user
          certificate.staff_review_status = (action == 'approve')

      certificate.remarks = remarks
      certificate.save()

      # Apply signature if approved
      if action == 'approve':
          signature_path = os.path.join(settings.BASE_DIR, 'mainapp', 'static', 'signatures', f'{group_name.lower()}_signature.png')
          
          if certificate.CertificateType.startswith('A_') and group_name == 'CEO':
              certificate.apply_signature('CEO', signature_path)
          elif certificate.CertificateType.startswith('B_'):
              if group_name == 'Staff' and not certificate.staff_signature_applied:
                  certificate.apply_signature('Staff', signature_path)
              elif group_name == 'CEO' and not certificate.ceo_signature_applied:
                  certificate.apply_signature('CEO', signature_path)
          elif certificate.CertificateType == 'C_Army':
              if group_name == 'register_head' and not certificate.register_head_signature_applied:
                  certificate.apply_signature('register_head', signature_path)
              elif group_name in ['CEO', 'Staff']:
                  if group_name == 'CEO' and not certificate.ceo_signature_applied:
                      certificate.apply_signature('CEO', signature_path)
                  elif group_name == 'Staff' and not certificate.staff_signature_applied:
                      certificate.apply_signature('Staff', signature_path)

      return redirect('main')

  context = {
      'certificate': certificate,
      'can_verify': can_verify,
      'group_name': group_name,
      'a_certificates': ['A_Army', 'A_AirForce', 'A_Navy'],
      'b_certificates': ['B_Army', 'B_AirForce', 'B_Navy'],
      'c_certificates': ['C_Army']
  }

  return render(request, 'verify_certificate.html', context)

from PIL import Image, ImageDraw, ImageFont
from mainapp.models import Certificate  # Import your Certificate model here

def generate_duplicate_certificate(request):
    if request.method == 'POST':
        certificate_number = request.POST.get('certificate_number')
        print(f"Certificate Number from POST: {certificate_number}")  # Debugging print
        
        try:
            certificate = Certificate.objects.get(certificate_number=certificate_number)
            print(f"Certificate found: {certificate}")  # Debugging print
            
            # Check if a final certificate exists
            if certificate.final_certificate:
                return render(request, 'show_certificate.html', {'certificate': certificate})
            else:
                return HttpResponse("No final certificate found for this certificate.")
        
        except Certificate.DoesNotExist:
            print("No Certificate matches the given query.")  # Debugging print
            return HttpResponse("No Certificate matches the given query.")
    
    return render(request, 'generate_certificate.html')
import PyPDF2
from io import BytesIO
from django.http import HttpResponse
def download_duplicate_certificate(request):
  if request.method == 'POST':
      certificate_id = request.POST.get('certificate_id')
      certificate = get_object_or_404(Certificate, id=certificate_id)
      
      # Open the PDF file
      pdf_file = open(certificate.final_certificate.path, 'rb')
      pdf_reader = PyPDF2.PdfReader(pdf_file)
      
      # Create a new PDF writer
      pdf_writer = PyPDF2.PdfWriter()
      
      # Create a new PDF canvas
      packet = BytesIO()
      can = canvas.Canvas(packet, pagesize=letter)
      
      # Draw the "Duplicate" text on the canvas
      can.setFont("Helvetica", 12)
      if Certificate.CertificateType == 'C_Army':
          can.drawString(400, 780, "Duplicate")
      else:
          can.drawString(50, 780, "Duplicate")
      
      # Save the canvas to a bytes buffer
      can.save()
      packet.seek(0)
      
      # Merge the canvas with each page of the original PDF
      new_pdf = PyPDF2.PdfReader(packet)
      for page_num in range(len(pdf_reader.pages)):
          page = pdf_reader.pages[page_num]
          page.merge_page(new_pdf.pages[0])
          pdf_writer.add_page(page)
      
      # Save the modified PDF to a temporary location
      temp_pdf_path = os.path.join(settings.MEDIA_ROOT, 'temp_duplicate_certificate.pdf')
      with open(temp_pdf_path, 'wb') as f:
          pdf_writer.write(f)
      
      # Serve the modified PDF for download
      with open(temp_pdf_path, 'rb') as f:
          response = HttpResponse(f.read(), content_type="application/pdf")
          response['Content-Disposition'] = 'attachment; filename="duplicate_certificate.pdf"'
          return response
  
  return HttpResponse("Invalid request method.")

def rejected_certificates_register_head(request):
    user = request.user
    is_clerk = user.groups.filter(name='Clerk').exists()
    rejected_certificates = Certificate.objects.filter(register_head_review_status=False)
    return render(request, 'rejected_certificates.html', {'certificates': rejected_certificates, 'role': 'ADG','is_clerk':is_clerk})

def rejected_certificates_ceo(request):
    user = request.user
    is_clerk = user.groups.filter(name='Clerk').exists()
    rejected_certificates = Certificate.objects.filter(ceo_review_status=False)
    return render(request, 'rejected_certificates.html', {'certificates': rejected_certificates, 'role': 'CO','is_clerk':is_clerk})

def rejected_certificates_staff(request):
    user = request.user
    is_clerk = user.groups.filter(name='Clerk').exists()
    rejected_certificates = Certificate.objects.filter(staff_review_status=False)
    return render(request, 'rejected_certificates.html', {'certificates': rejected_certificates, 'role': 'Group Commander','is_clerk':is_clerk})



import logging

logger = logging.getLogger(__name__)

def signed_certificates_view(request):
    logger.debug("Entered signed_certificates_view")
    signed_certificates = Certificate.objects.filter(is_signed=True)
    logger.debug(f"Fetching signed certificates, count: {signed_certificates.count()}")

    for cert in signed_certificates:
        logger.debug(f"Signed certificate: {cert.Name}, Serial Number: {cert.serial_number}, is_signed: {cert.is_signed}")

    context = {
        'certificates': signed_certificates
    }
    
    return render(request, 'signed_certificates.html', context)


def signed_certificates_viewtrue(request):
    signed_certificates = Certificate.objects.filter(is_signed=True)
    return render(request, 'signed_certificatestrue.html', {'certificates': signed_certificates})

def unsigned_certificates_view(request):
    certificates = Certificate.objects.filter(is_signed=False)
    return render(request, 'unsigned_certificates.html', {'certificates': certificates})