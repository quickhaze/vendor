from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Vendor , OTPVerification, VendorProfile

class VendorAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password' , )}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_approved')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

admin.site.register(Vendor, VendorAdmin)
admin.site.register(OTPVerification)
admin.site.register(VendorProfile)
