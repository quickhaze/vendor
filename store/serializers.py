from rest_framework import serializers
from .models import Vendor, VendorProfile, Artwork, VendorSale, Payment, Tender
from .utils import send_otp_email

class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = ['id', 'email', 'username','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        vendor = Vendor.objects.create_user(**validated_data) 
        vendor.save_otp()  
        return vendor

class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = '__all__'

class ArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = '__all__'

class VendorSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorSale
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class TenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = '__all__'
