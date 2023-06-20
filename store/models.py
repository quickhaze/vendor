from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.forms import ValidationError
from django.db import models
from django.utils import timezone
from .utils import send_otp_email


class Vendor(AbstractUser):
    is_approved = models.BooleanField(default=False)

    def save_otp(self):
        otp = getattr(self, 'otpverification', None)
        if otp: 
            otp.delete()
        otp_verification = OTPVerification.objects.create(vendor=self)
        otp_verification.send_otp()  # Send OTP via email or any other method
    
    def __str__(self) -> str:
        return self.email

class OTPVerification(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    verified =  models.BooleanField(default=False)
    expired =  models.BooleanField(default=False)

    def send_otp(self):
        self.otp = send_otp_email(self.vendor.email)
        self.save()

    def verify_otp(self):
        self.verified  = True
        self.save()
        self.create_vendor_profile()
    def __str__(self):
        return f"OTP: {self.otp} - Vendor: {self.vendor.username}"

    def create_vendor_profile(self):
      VendorProfile.objects.create(
          vendor = self.vendor
      )  
class VendorProfile(models.Model):
    WORKING = 'working'
    STUDYING = 'studying'
    OTHER = 'other'
    
    WORK_STATUS_CHOICES = [
        (WORKING, 'Working'),
        (STUDYING, 'Studying'),
        (OTHER, 'Other'),
    ]
    
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    working_or_studying = models.CharField(max_length=255, choices=WORK_STATUS_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.vendor}"


class Artwork(models.Model):
    vendor_profile = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='artwork_images')
    theme = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    medium = models.CharField(max_length=255)
    
    def clean(self):
        super().clean()
        if self.vendor_profile.artwork_set.count() >= 20:
            raise ValidationError("Maximum limit of 20 artworks per vendor profile reached.")
    
    def __str__(self):
        return self.theme

class VendorSale(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Payment(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Tender(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
