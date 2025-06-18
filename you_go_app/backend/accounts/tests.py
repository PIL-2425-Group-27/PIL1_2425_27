# accounts/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch
from accounts.models import UserProfile, Vehicle, KYC, TrackingGPS

User = get_user_model()

class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'phone_number': '+22612345678',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        
    def test_user_registration(self):
        """Test user registration creates user and profile"""
        url = reverse('register')
        response = self.client.post(url, self.user_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())
        
        # Check if profile was created
        user = User.objects.get(email=self.user_data['email'])
        self.assertTrue(hasattr(user, 'profile'))
        
    def test_role_update(self):
        """Test role update functionality"""
        user = User.objects.create_user(
            email='test@example.com',
            phone_number='+22612345678',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)
        
        url = reverse('role')
        response = self.client.post(url, {'role': 'CONDUCTEUR'})
        
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.role, 'CONDUCTEUR')
        
    def test_invalid_role_update(self):
        """Test invalid role rejection"""
        user = User.objects.create_user(
            email='test@example.com',
            phone_number='+22612345678',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)
        
        url = reverse('role')
        response = self.client.post(url, {'role': 'INVALID'})
        
        self.assertEqual(response.status_code, 400)

class PasswordResetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            phone_number='+22612345678',
            password='oldpass123'
        )
        
    @patch('accounts.views.send_transactional_email')
    def test_password_reset_request(self, mock_send_email):
        """Test password reset email sending"""
        url = reverse('request-password-reset')
        response = self.client.post(url, {'email': self.user.email})
        
        self.assertEqual(response.status_code, 200)
        mock_send_email.assert_called_once()
        
        # Check if reset code was generated
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.reset_code)
        
    def test_password_reset_rate_limiting(self):
        """Test rate limiting for password reset"""
        url = reverse('request-password-reset')
        
        # Make 4 requests (exceeding limit of 3)
        for _ in range(4):
            response = self.client.post(url, {'email': self.user.email})
            
        # Last request should be rate limited
        self.assertEqual(response.status_code, 429)

class ProfileTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            phone_number='+22612345678',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_profile_creation(self):
        """Test profile is created automatically"""
        url = reverse('profile')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())
        
    def test_profile_update(self):
        """Test profile update"""
        url = reverse('profile')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01'
        }
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, 200)
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.first_name, 'John')

class VehicleTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            phone_number='+22612345678',
            password='testpass123',
            role='CONDUCTEUR'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_vehicle_creation(self):
        """Test vehicle creation"""
        url = reverse('vehicle')
        data = {
            'brand': 'Toyota',
            'model': 'Camry',
            'license_plate': 'AB-123-CD',
            'seats_available': 4
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Vehicle.objects.filter(owner=self.user).exists())
        
    def test_duplicate_vehicle_prevention(self):
        """Test that user can't create multiple vehicles"""
        # Create first vehicle
        Vehicle.objects.create(
            owner=self.user,
            brand='Toyota',
            model='Camry',
            license_plate='AB-123-CD',
            seats_available=4
        )
        
        # Try to create second vehicle
        url = reverse('vehicle')
        data = {
            'brand': 'Honda',
            'model': 'Civic',
            'license_plate': 'EF-456-GH',
            'seats_available': 3
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 400)

class KYCTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            phone_number='+22612345678',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            phone_number='+22612345679',
            password='adminpass123'
        )
        
    def test_kyc_creation(self):
        """Test KYC creation on first access"""
        self.client.force_authenticate(user=self.user)
        url = reverse('kyc')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(KYC.objects.filter(user=self.user).exists())
        
    @patch('accounts.views.send_transactional_email')
    def test_kyc_admin_approval(self, mock_send_email):
        """Test KYC approval by admin"""
        kyc = KYC.objects.create(user=self.user)
        self.client.force_authenticate(user=self.admin_user)
        
        url = reverse('kyc-admin', args=[self.user.id])
        response = self.client.post(url, {'action': 'approve'})
        
        self.assertEqual(response.status_code, 200)
        kyc.refresh_from_db()
        self.assertEqual(kyc.status, 'APPROVED')
        mock_send_email.assert_called_once()

class GPSTrackingTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            phone_number='+22612345678',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            phone_number='+22612345679',
            password='testpass123'
        )
        
    def test_tracking_consent_update(self):
        """Test updating tracking consent"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('update-tracking-consent')
        response = self.client.patch(url, {'consent_tracking': True})
        
        self.assertEqual(response.status_code, 200)
        tracking = TrackingGPS.objects.get(user=self.user1)
        self.assertTrue(tracking.consent_tracking)
        
    def test_gps_position_update(self):
        """Test GPS position update"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('gps')
        data = {
            'last_latitude': 6.3703,
            'last_longitude': 2.3912
        }
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, 200)
        tracking = TrackingGPS.objects.get(user=self.user1)
        self.assertEqual(float(tracking.last_latitude), 6.3703)

class AccountDeletionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            phone_number='+22612345678',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_secure_account_deletion(self):
        """Test secure account deletion with password verification"""
        url = reverse('delete-account')
        response = self.client.delete(url, {'password': 'testpass123'})
        
        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())
        
    def test_account_deletion_wrong_password(self):
        """Test account deletion fails with wrong password"""
        url = reverse('delete-account')
        response = self.client.delete(url, {'password': 'wrongpass'})
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(User.objects.filter(id=self.user.id).exists())