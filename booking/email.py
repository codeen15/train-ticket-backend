import base64
import qrcode
from django.core.mail import EmailMessage
from django.core.files.base import ContentFile
from io import BytesIO
from django.conf import settings

def generate_qr_code(bookingID: str):
    # Generate QR code
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10, border=4)
    qr.add_data(bookingID)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return img_io

def send_qr_code_email(bookingID, recipient_name, recipient_email):
    qr_code_image = generate_qr_code(str(bookingID))

    subject = f'Hi {recipient_name}, Your train ticket booking has been confirmed!'
    message = 'Here is your booking details: {}'.format(bookingID)
    qr_code_base64 = base64.b64encode(qr_code_image.getvalue()).decode('utf-8')
    
    # Send the email with the QR code
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email]
    )

    email.content_subtype = 'html' 
    email.body = f'<p>{message}</p><img src="data:image/png;base64,{qr_code_base64}"/>'
    email.send(fail_silently=False)
    print('Email sent to ' + recipient_email)