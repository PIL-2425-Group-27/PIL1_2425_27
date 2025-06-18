# accounts/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Import views
from .views import (
    # Authentication views
    RegisterView,
    RoleView,  # Fixed naming convention
    LogoutView,
    LoginView,  # If you have a custom login view, otherwise use TokenObtainPairView
    
    # Password reset views
    RequestPasswordResetView,
    ResetPasswordView,
    
    # Profile and user management
    ProfileView,
    SecureDeleteAccountView,
    ThemePreferenceUpdateView,
    
    # Vehicle management
    VehicleView,
    
    # KYC management
    KYCView,
    KYCAdminView,
    
    # GPS tracking views
    TrackingGPSView,
    GPSHistoryView,
    update_tracking_consent,
    get_user_tracking_position,
)

app_name = 'accounts'  # Add app namespace

urlpatterns = [
    # ==========================================
    # AUTHENTICATION ENDPOINTS
    # ==========================================
    
    # User registration
    path('register/', RegisterView.as_view(), name='register'),
    
    # Role management (driver, passenger)
    path('role/', RoleView.as_view(), name='role'),
    
    # JWT Authentication
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # ==========================================
    # PASSWORD MANAGEMENT
    # ==========================================
    
    # Password reset workflow
    path('password/reset/request/', RequestPasswordResetView.as_view(), name='request_password_reset'),
    path('password/reset/confirm/', ResetPasswordView.as_view(), name='confirm_password_reset'),
    
    # ==========================================
    # USER PROFILE MANAGEMENT
    # ==========================================
    
    # User profile CRUD
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Account deletion
    path('account/delete/', SecureDeleteAccountView.as_view(), name='delete_account'),
    
    # Theme preferences
    path('theme/', ThemePreferenceUpdateView.as_view(), name='theme_preference'),
    
    # ==========================================
    # VEHICLE MANAGEMENT
    # ==========================================
    
    # Vehicle registration and management
    path('vehicle/', VehicleView.as_view(), name='vehicle'),
    
    # ==========================================
    # KYC (KNOW YOUR CUSTOMER) MANAGEMENT
    # ==========================================
    
    # User KYC submission and status
    path('kyc/', KYCView.as_view(), name='kyc'),
    
    # Admin KYC validation
    path('kyc/admin/<int:user_id>/', KYCAdminView.as_view(), name='kyc_admin'),
    
    # ==========================================
    # GPS TRACKING SYSTEM
    # ==========================================
    
    # GPS position tracking
    path('gps/', TrackingGPSView.as_view(), name='gps_tracking'),
    
    # GPS tracking history
    path('gps/history/', GPSHistoryView.as_view(), name='gps_history'),
    
    # GPS tracking consent management
    path('gps/consent/', update_tracking_consent, name='gps_consent'),
    
    # Get specific user's tracking position (for ride sharing)
    path('gps/user/<int:user_id>/', get_user_tracking_position, name='user_gps_position'),
]

# ==========================================
# URL PATTERNS DOCUMENTATION
# ==========================================
"""
Authentication Endpoints:
- POST /accounts/register/ - Register new user
- POST /accounts/role/ - Update user role (driver/passenger)
- POST /accounts/login/ - Login (get JWT tokens)
- POST /accounts/token/refresh/ - Refresh JWT token
- POST /accounts/logout/ - Logout (blacklist token)

Password Management:
- POST /accounts/password/reset/request/ - Request password reset
- POST /accounts/password/reset/confirm/ - Confirm password reset with code

Profile Management:
- GET/PATCH /accounts/profile/ - Get/update user profile
- DELETE /accounts/account/delete/ - Secure account deletion
- POST /accounts/theme/ - Update theme preference

Vehicle Management:
- GET/POST/PATCH /accounts/vehicle/ - Vehicle CRUD operations

KYC Management:
- GET/PATCH /accounts/kyc/ - User KYC operations
- POST /accounts/kyc/admin/<user_id>/ - Admin KYC validation

GPS Tracking:
- GET/PATCH /accounts/gps/ - GPS position tracking
- GET /accounts/gps/history/ - GPS tracking history
- PATCH /accounts/gps/consent/ - Update tracking consent
- GET /accounts/gps/user/<user_id>/ - Get user's position (for ride sharing)
"""