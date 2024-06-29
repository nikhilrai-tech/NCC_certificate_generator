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
    c = canvas.Canvas(buffer, pagesize=A4)

    # Calculate A4 page dimensions in points (1 inch = 72 points)
    page_width, page_height = A4

    # Margin settings in points
    margin_x = 50
    margin_y = 50

    # Iterate through each certificate
    for certificate in certificates:
        # Load the certificate image
        if certificate.final_certificate:
            img_path = certificate.final_certificate.path
            img = Image.open(img_path)

            # Calculate image dimensions to fit within the A4 page
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height

            # Calculate scaling factor to fit the image within the A4 page
            if aspect_ratio > 1:
                # Landscape orientation
                if img_width > page_width - 2 * margin_x:
                    img_width = page_width - 2 * margin_x
                    img_height = img_width / aspect_ratio
            else:
                # Portrait orientation
                if img_height > page_height - 2 * margin_y:
                    img_height = page_height - 2 * margin_y
                    img_width = img_height * aspect_ratio

            # Calculate position for the image on the page
            x = (page_width - img_width) / 2
            y = (page_height - img_height) / 2

            # Draw the image on the PDF page
            c.drawImage(img_path, x, y, width=img_width, height=img_height)
            c.showPage()  # Add a new page for the next certificate

    c.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_certificates.pdf"'
    return response

def certificate_success(request):
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
            return render(request, 'signup_form.html', {'form': form, 'role': 'Commanding Staff', 'errors': form.errors})
    else:
        form = StaffSignUpForm()
    return render(request, 'signup_form.html', {'form': form, 'role': 'Commanding Staff'})

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
        else:
            return HttpResponse('Invalid login credentials')
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def signuppage(request):
    return render(request, 'signuppage.html')

def forgotpass(request):
    return render(request, 'forgotpass.html')


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
            return render(request, 'signuphead_form.html', {'form': form, 'role': 'state head', 'errors': form.errors})
    else:
        form = headSignUpForm()
    return render(request, 'signuphead_form.html', {'form': form, 'role': 'state head'})




def dashboard(request):
    return render(request,"dashboard.html")


def mintemplate(request):
    return render(request,"maintemp.html")


def admincard(request):
    return render(request,"admincard.html")