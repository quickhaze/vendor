from django.urls import path, include
from rest_framework import routers
from .views import VendorViewSet, VendorProfileViewSet#, ArtworkViewSet, VendorSaleViewSet, PaymentViewSet, TenderViewSet

router = routers.DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'vendor-profiles', VendorProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    # Other URL patterns
    path('api/vendor/login/', VendorViewSet.as_view({'post': 'login'}), name='vendor-login'),
    path('api/vendor/verify-otp/', VendorViewSet.as_view({'post': 'verify_otp'}), name='vendor-verify-otp'),
    path('api/vendor/resend-otp/', VendorViewSet.as_view({'post': 'resend_otp'}), name='vendor-resend-otp'),
] + router.urls

# router.register(r'artworks', ArtworkViewSet)
# router.register(r'vendor-sales', VendorSaleViewSet)
# router.register(r'payments', PaymentViewSet)
# router.register(r'tenders', TenderViewSet)