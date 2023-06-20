from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Vendor, VendorProfile, Artwork, VendorSale, Payment, Tender
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
# from .serializers import VendorSerializer, VendorProfileSerializer, ArtworkSerializer, VendorSaleSerializer, PaymentSerializer, TenderSerializer
from .serializers import (
    VendorSerializer,
  VendorProfileSerializer, ArtworkSerializer ) #, VendorSaleSerializer, PaymentSerializer, TenderSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.utils import timezone

from rest_framework.decorators import action


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        self.request._mutable = True
        self.request.data['username'] = self.request.data['email']
        self.request._mutable = False
        return context

    def auth_user(self):
        email = self.request.data.get("email")
        password = self.request.data.get("password")

        # Authenticate the vendor
        user = authenticate(self.request, username=email, password=password)
        return user

    @action(methods=["POST"], detail=False)
    def login(self, request):
        # Authenticate the vendor
        user = self.auth_user()
        if user is not None and user.is_active:
            # import pdb; pdb.set_trace()
            if hasattr(user, "vendorprofile"):
                if not user.is_approved:
                    message = "Your account has not been approved"
                # Vendor is authenticated, active, and has vendor-specific attributes
                else:
                    login(request, user)
                    message = "Login successful"
                return Response({"message": message}, status=status.HTTP_200_OK)
            elif not user.otpverification.verified:
                message = "OTP not verified"
            else:
                # Authenticated user, but not a vendor user
                message = "You are not authorized to login as a vendor"
            return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)
        else:
            # Invalid credentials or inactive user
            return Response(
                {"message": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    @action(detail=True, methods=["POST"])
    def verify_otp(self, request,):
        user = self.auth_user()
        otp = request.data.get('otp', 0)
        if user:
            if user.otpverification.otp == str(otp):
                if user.otpverification.verified:
                    message = "Already Verified"
                    _status = status.HTTP_200_OK
                elif user.otpverification.expired or  ( timezone.now() - user.otpverification.created_at).seconds > 600:
                    message = "OTP Expired"
                    _status=status.HTTP_400_BAD_REQUEST
                else:
                    user.otpverification.verify_otp()
                    message = "OTP Verified"
                    _status = status.HTTP_201_CREATED
            else:
                return Response({'detail': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = "Invalid credentials"
            _status = status.HTTP_401_UNAUTHORIZED
        return Response({'detail': message}, status=_status)

    @action(detail=True, methods=["POST"])
    def resend_otp(self, request,):
        user = self.auth_user()
        if not user:
            message = "Invalid credentials"
            _status = status.HTTP_401_UNAUTHORIZED
        else:
            user.save_otp()
            message = "Resent"
            _status = status.HTTP_201_CREATED
        return Response({'detail': message}, status=_status)

class VendorLogin(APIView):

    def post(self, request):
        return Response()


class VendorProfileViewSet(viewsets.ModelViewSet):
    queryset = VendorProfile.objects.all()
    serializer_class = VendorProfileSerializer
    authentication_classes = [SessionAuthentication]  # Add authentication class
    permission_classes = [IsAuthenticated] 

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class ArtworkViewSet(viewsets.ModelViewSet):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer

# class VendorSaleViewSet(viewsets.ModelViewSet):
#     queryset = VendorSale.objects.all()
#     serializer_class = VendorSaleSerializer

# class PaymentViewSet(viewsets.ModelViewSet):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer

# class TenderViewSet(viewsets.ModelViewSet):
#     queryset = Tender.objects.all()
#     serializer_class = TenderSerializer
