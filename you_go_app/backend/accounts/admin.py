from django.contrib import admin
from .models import User, UserProfile, Vehicle, KYC, TrackingGPS

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone_number', 'role', 'is_kyc_validated', 'is_active')
    search_fields = ('email', 'username', 'phone_number')
    list_filter = ('role', 'is_active', 'is_kyc_validated')
    readonly_fields = ('date_joined', 'last_login')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_start_point', 'default_end_point', 'consent_tracking')
    search_fields = ('user__email',)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('owner', 'brand', 'model', 'license_plate', 'seats_available')
    search_fields = ('license_plate', 'owner__email')

@admin.register(KYC)
class KYCAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'is_kyc_validated', 'created_at', 'validated_at')
    list_filter = ('status',)
    search_fields = ('user__email',)
    actions = ['valider_kyc', 'rejeter_kyc']

    def valider_kyc(self, request, queryset):
        for kyc in queryset:
            kyc.approve()
        self.message_user(request, "KYC validés.")

    def rejeter_kyc(self, request, queryset):
        for kyc in queryset:
            kyc.reject("Rejeté par admin")
        self.message_user(request, "KYC rejetés.")

@admin.register(TrackingGPS)
class TrackingAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_latitude', 'last_longitude', 'last_update')
    readonly_fields = ('last_update',)
