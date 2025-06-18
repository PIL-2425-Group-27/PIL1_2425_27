from django.contrib import admin
'''from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.utils import timezone
from .models import User, UserProfile, Vehicle, KYC, TrackingGPS, GPSHistory

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email', 'username', 'phone_number', 'role', 
        'is_kyc_validated', 'is_active', 'date_joined_formatted',
        'last_login_formatted'
    )
    list_display_links = ('email', 'username')
    search_fields = ('email', 'username', 'phone_number', 'first_name', 'last_name')
    list_filter = (
        'role', 'is_active', 'is_kyc_validated', 'is_staff', 
        'date_joined', 'last_login', 'theme_preference'
    )
    readonly_fields = ('date_joined', 'last_login', 'password')
    ordering = ('-date_joined',)
    list_per_page = 25
    
    # Custom fieldsets for better organization
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('username', 'email', 'phone_number', 'first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Informations importantes', {
            'fields': ('role', 'is_kyc_validated', 'theme_preference')
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
        ('Sécurité', {
            'fields': ('password',),
            'classes': ('collapse',)
        })
    )
    
    add_fieldsets = (
        ('Créer un nouvel utilisateur', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2', 'role'),
        }),
    )
    
    actions = ['activate_users', 'deactivate_users', 'validate_kyc_bulk']
    
    def date_joined_formatted(self, obj):
        return obj.date_joined.strftime('%d/%m/%Y à %H:%M') if obj.date_joined else '-'
    date_joined_formatted.short_description = 'Date d\'inscription'
    
    def last_login_formatted(self, obj):
        if obj.last_login:
            return obj.last_login.strftime('%d/%m/%Y à %H:%M')
        return 'Jamais connecté'
    last_login_formatted.short_description = 'Dernière connexion'
    
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} utilisateur(s) activé(s).')
    activate_users.short_description = 'Activer les utilisateurs sélectionnés'
    
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} utilisateur(s) désactivé(s).')
    deactivate_users.short_description = 'Désactiver les utilisateurs sélectionnés'
    
    def validate_kyc_bulk(self, request, queryset):
        count = 0
        for user in queryset:
            if hasattr(user, 'kyc') and user.kyc.status != 'APPROVED':
                user.kyc.approve()
                count += 1
        self.message_user(request, f'{count} KYC validé(s).')
    validate_kyc_bulk.short_description = 'Valider les KYC des utilisateurs sélectionnés'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user_email', 'full_name', 'date_of_birth', 
        'default_start_point', 'default_end_point', 
        'consent_tracking_display', 'profile_completion'
    )
    list_display_links = ('user_email', 'full_name')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    list_filter = ('consent_tracking', 'user__role')
    readonly_fields = ('last_modified_name', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'bio')
        }),
        ('Préférences de trajet', {
            'fields': ('default_start_point', 'default_end_point')
        }),
        ('Confidentialité', {
            'fields': ('consent_tracking',)
        }),
        ('Métadonnées', {
            'fields': ('last_modified_name', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'
    
    def full_name(self, obj):
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        return obj.user.username
    full_name.short_description = 'Nom complet'
    
    def consent_tracking_display(self, obj):
        if obj.consent_tracking:
            return format_html('<span style="color: green;">✓ Autorisé</span>')
        return format_html('<span style="color: red;">✗ Refusé</span>')
    consent_tracking_display.short_description = 'Suivi GPS'
    
    def profile_completion(self, obj):
        fields = ['first_name', 'last_name', 'date_of_birth', 'bio']
        completed = sum(1 for field in fields if getattr(obj, field))
        percentage = int((completed / len(fields)) * 100)
        
        color = 'green' if percentage >= 75 else 'orange' if percentage >= 50 else 'red'
        return format_html(
            '<span style="color: {};">{}/{}  ({}%)</span>',
            color, completed, len(fields), percentage
        )
    profile_completion.short_description = 'Complétion du profil'

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'license_plate', 'owner_email', 'brand_model', 
        'seats_available', 'vehicle_status', 'created_at_formatted'
    )
    list_display_links = ('license_plate',)
    search_fields = ('license_plate', 'owner__email', 'brand', 'model')
    list_filter = ('brand', 'seats_available', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Propriétaire', {
            'fields': ('owner',)
        }),
        ('Informations du véhicule', {
            'fields': ('brand', 'model', 'license_plate', 'color', 'year')
        }),
        ('Capacité', {
            'fields': ('seats_available',)
        }),
        ('Documents', {
            'fields': ('insurance_document', 'registration_document'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def owner_email(self, obj):
        return obj.owner.email
    owner_email.short_description = 'Propriétaire'
    owner_email.admin_order_field = 'owner__email'
    
    def brand_model(self, obj):
        return f"{obj.brand} {obj.model}"
    brand_model.short_description = 'Marque/Modèle'
    
    def vehicle_status(self, obj):
        if obj.owner.is_kyc_validated:
            return format_html('<span style="color: green;">✓ Validé</span>')
        return format_html('<span style="color: orange;">⏳ En attente KYC</span>')
    vehicle_status.short_description = 'Statut'
    
    def created_at_formatted(self, obj):
        return obj.created_at.strftime('%d/%m/%Y') if obj.created_at else '-'
    created_at_formatted.short_description = 'Date d\'ajout'
    created_at_formatted.admin_order_field = 'created_at'

@admin.register(KYC)
class KYCAdmin(admin.ModelAdmin):
    list_display = (
        'user_email', 'status_display', 'created_at_formatted', 
        'validated_at_formatted', 'validator_info'
    )
    list_display_links = ('user_email',)
    list_filter = ('status', 'created_at', 'validated_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'validated_at', 'validated_by')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Documents', {
            'fields': ('identity_document', 'address_proof', 'additional_documents')
        }),
        ('Statut', {
            'fields': ('status', 'rejection_reason')
        }),
        ('Validation', {
            'fields': ('validated_at', 'validated_by'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    actions = ['approve_kyc', 'reject_kyc', 'reset_kyc']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Utilisateur'
    user_email.admin_order_field = 'user__email'
    
    def status_display(self, obj):
        colors = {
            'PENDING': 'orange',
            'APPROVED': 'green',
            'REJECTED': 'red'
        }
        icons = {
            'PENDING': '⏳',
            'APPROVED': '✅',
            'REJECTED': '❌'
        }
        return format_html(
            '<span style="color: {};">{} {}</span>',
            colors.get(obj.status, 'black'),
            icons.get(obj.status, '?'),
            obj.get_status_display()
        )
    status_display.short_description = 'Statut'
    
    def created_at_formatted(self, obj):
        return obj.created_at.strftime('%d/%m/%Y à %H:%M')
    created_at_formatted.short_description = 'Demande créée'
    created_at_formatted.admin_order_field = 'created_at'
    
    def validated_at_formatted(self, obj):
        if obj.validated_at:
            return obj.validated_at.strftime('%d/%m/%Y à %H:%M')
        return '-'
    validated_at_formatted.short_description = 'Validée le'
    
    def validator_info(self, obj):
        if obj.validated_by:
            return obj.validated_by.username
        return '-'
    validator_info.short_description = 'Validé par'
    
    def approve_kyc(self, request, queryset):
        count = 0
        for kyc in queryset.filter(status='PENDING'):
            kyc.approve()
            count += 1
        self.message_user(request, f'{count} KYC approuvé(s).')
    approve_kyc.short_description = 'Approuver les KYC sélectionnés'
    
    def reject_kyc(self, request, queryset):
        count = 0
        for kyc in queryset.filter(status='PENDING'):
            kyc.reject("Rejeté en lot par l'administrateur")
            count += 1
        self.message_user(request, f'{count} KYC rejeté(s).')
    reject_kyc.short_description = 'Rejeter les KYC sélectionnés'
    
    def reset_kyc(self, request, queryset):
        count = queryset.update(status='PENDING', validated_at=None, validated_by=None)
        self.message_user(request, f'{count} KYC remis en attente.')
    reset_kyc.short_description = 'Remettre en attente'

@admin.register(TrackingGPS)
class TrackingGPSAdmin(admin.ModelAdmin):
    list_display = (
        'user_email', 'current_position', 'consent_status', 
        'last_update_formatted', 'tracking_activity'
    )
    list_display_links = ('user_email',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    list_filter = ('consent_tracking', 'last_update')
    readonly_fields = ('last_update', 'created_at')
    ordering = ('-last_update',)
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Position actuelle', {
            'fields': ('last_latitude', 'last_longitude')
        }),
        ('Paramètres', {
            'fields': ('consent_tracking',)
        }),
        ('Métadonnées', {
            'fields': ('last_update', 'created_at'),
            'classes': ('collapse',)
        })
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Utilisateur'
    user_email.admin_order_field = 'user__email'
    
    def current_position(self, obj):
        if obj.last_latitude and obj.last_longitude:
            # Create a link to Google Maps
            maps_url = f"https://www.google.com/maps?q={obj.last_latitude},{obj.last_longitude}"
            return format_html(
                '<a href="{}" target="_blank">📍 {:.4f}, {:.4f}</a>',
                maps_url, float(obj.last_latitude), float(obj.last_longitude)
            )
        return '-'
    current_position.short_description = 'Position'
    
    def consent_status(self, obj):
        if obj.consent_tracking:
            return format_html('<span style="color: green;">✓ Autorisé</span>')
        return format_html('<span style="color: red;">✗ Refusé</span>')
    consent_status.short_description = 'Consentement'
    
    def last_update_formatted(self, obj):
        if obj.last_update:
            delta = timezone.now() - obj.last_update
            if delta.seconds < 3600:  # Less than 1 hour
                return format_html(
                    '<span style="color: green;">{}</span>',
                    obj.last_update.strftime('%d/%m/%Y à %H:%M')
                )
            elif delta.days < 1:  # Less than 1 day
                return format_html(
                    '<span style="color: orange;">{}</span>',
                    obj.last_update.strftime('%d/%m/%Y à %H:%M')
                )
            else:
                return format_html(
                    '<span style="color: red;">{}</span>',
                    obj.last_update.strftime('%d/%m/%Y à %H:%M')
                )
        return '-'
    last_update_formatted.short_description = 'Dernière MAJ'
    
    def tracking_activity(self, obj):
        if not obj.last_update:
            return format_html('<span style="color: gray;">Jamais actif</span>')
        
        delta = timezone.now() - obj.last_update
        if delta.seconds < 300:  # 5 minutes
            return format_html('<span style="color: green;">🟢 En ligne</span>')
        elif delta.seconds < 3600:  # 1 hour
            return format_html('<span style="color: orange;">🟡 Récent</span>')
        else:
            return format_html('<span style="color: red;">🔴 Inactif</span>')
    tracking_activity.short_description = 'Activité'

# Register GPSHistory if you have this model
try:
    from .models import GPSHistory
    
    @admin.register(GPSHistory)
    class GPSHistoryAdmin(admin.ModelAdmin):
        list_display = ('user_email', 'position', 'timestamp_formatted')
        list_filter = ('timestamp',)
        search_fields = ('user__email',)
        readonly_fields = ('timestamp',)
        ordering = ('-timestamp',)
        
        def user_email(self, obj):
            return obj.user.email
        user_email.short_description = 'Utilisateur'
        
        def position(self, obj):
            return f"{obj.latitude:.4f}, {obj.longitude:.4f}"
        position.short_description = 'Position'
        
        def timestamp_formatted(self, obj):
            return obj.timestamp.strftime('%d/%m/%Y à %H:%M:%S')
        timestamp_formatted.short_description = 'Horodatage'
        
except ImportError:
    pass

# Customize Admin Site
admin.site.site_header = "YouGo - Administration"
admin.site.site_title = "YouGo Admin"
admin.site.index_title = "Tableau de bord administrateur"

'''