from django.core.mail import send_mail
# from django_otp import devices
import random
def send_otp_email(user_email):
    # otp_device = devices.default_device(user_email)
    # otp_device.generate_challenge()
    # otp = otp_device.challenge
    otp = str(random.randint(100000, 999999))
    # Modify the email subject and message as desired
    subject = 'OTP Verification'
    message = f'Your OTP is: {otp}'
    sender_email = 'your_email@example.com'
    recipient_email = user_email

    send_mail(subject, message, sender_email, [recipient_email])
    return otp