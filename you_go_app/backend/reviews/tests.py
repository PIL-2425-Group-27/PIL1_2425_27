from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import IntegrityError
from unittest.mock import patch
import json

from .models import Review
from .signals import update_reviewed_user_badge

User = get_user_model()

class ReviewModelTests(TestCase):
    def setUp(self):
        self.reviewer = User.objects.create_user(
            username='reviewer',
            email='reviewer@test.com',
            password='testpass123'
        )
        self.reviewed_user = User.objects.create_user(
            username='reviewed',
            email='reviewed@test.com',
            password='testpass123'
        )
    
    def test_review_creation(self):
        """Test basic review creation"""
        review = Review.objects.create(
            reviewer=self.reviewer,
            reviewed_user=self.reviewed_user,
            rating=5,
            comment="Great user!"
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Great user!")
        self.assertTrue(review.is_active)
    
    def test_review_str_representation(self):
        """Test string representation of review"""
        review = Review.objects.create(
            reviewer=self.reviewer,
            reviewed_user=self.reviewed_user,
            rating=4
        )
        expected = f"{self.reviewer.username} -> {self.reviewed_user.username} (4/5)"
        self.assertEqual(str(review), expected)
    
    def test_rating_validation(self):
        """Test rating must be between 1 and 5"""
        # This would need to be implemented in the model
        with self.assertRaises(Exception):  # Adjust based on your validation
            Review.objects.create(
                reviewer=self.reviewer,
                reviewed_user=self.reviewed_user,
                rating=6
            )
    
    def test_self_review_prevention(self):
        """Test users cannot review themselves"""
        # This would need to be implemented in the model
        with self.assertRaises(Exception):  # Adjust based on your validation
            Review.objects.create(
                reviewer=self.reviewer,
                reviewed_user=self.reviewer,
                rating=5
            )

class ReviewSignalTests(TestCase):
    def setUp(self):
        self.reviewer = User.objects.create_user(
            username='reviewer',
            email='reviewer@test.com',
            password='testpass123'
        )
        self.reviewed_user = User.objects.create_user(
            username='reviewed',
            email='reviewed@test.com',
            password='testpass123'
        )
    
    @patch.object(User, 'update_reliability')
    @patch.object(User, 'save')
    def test_signal_triggers_on_review_creation(self, mock_save, mock_update):
        """Test that signal fires when review is created"""
        Review.objects.create(
            reviewer=self.reviewer,
            reviewed_user=self.reviewed_user,
            rating=5,
            comment="Great user!"
        )
        
        mock_update.assert_called_once()
        mock_save.assert_called_once()
    
    @patch.object(User, 'update_reliability')
    def test_signal_does_not_trigger_on_update(self, mock_update):
        """Test that signal only fires on creation, not updates"""
        review = Review.objects.create(
            reviewer=self.reviewer,
            reviewed_user=self.reviewed_user,
            rating=5
        )
        
        mock_update.reset_mock()
        review.comment = "Updated comment"
        review.save()
        
        mock_update.assert_not_called()

class ReviewViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.reviewer = User.objects.create_user(
            username='reviewer',
            email='reviewer@test.com',
            password='testpass123'
        )
        self.reviewed_user = User.objects.create_user(
            username='reviewed',
            email='reviewed@test.com',
            password='testpass123'
        )
        
        # Create some test reviews
        Review.objects.create(
            reviewer=self.reviewer,
            reviewed_user=self.reviewed_user,
            rating=5,
            comment="Excellent!"
        )
        Review.objects.create(
            reviewer=self.reviewed_user,
            reviewed_user=self.reviewer,
            rating=4,
            comment="Good user"
        )
    
    def test_review_creation_authenticated(self):
        """Test review creation with authenticated user"""
        self.client.login(username='reviewer', password='testpass123')
        
        data = {
            'reviewed_user': self.reviewed_user.id,
            'rating': 4,
            'comment': 'Test review'
        }
        
        response = self.client.post(reverse('create-review'), data)
        # Adjust assertion based on your view's response
        self.assertEqual(response.status_code, 201)  # or 200, 302 depending on implementation
    
    def test_review_creation_unauthenticated(self):
        """Test review creation fails without authentication"""
        data = {
            'reviewed_user': self.reviewed_user.id,
            'rating': 4,
            'comment': 'Test review'
        }
        
        response = self.client.post(reverse('create-review'), data)
        self.assertEqual(response.status_code, 401)  # or 403, 302 depending on implementation
    
    def test_user_reviews_list(self):
        """Test retrieving reviews for a specific user"""
        response = self.client.get(
            reverse('user-reviews', kwargs={'user_id': self.reviewed_user.id})
        )
        self.assertEqual(response.status_code, 200)
        
        # If returning JSON
        if response.content_type == 'application/json':
            data = json.loads(response.content)
            self.assertIn('reviews', data)
    
    def test_global_stats_view(self):
        """Test global statistics endpoint"""
        response = self.client.get(reverse('global-user-stats'))
        self.assertEqual(response.status_code, 200)
        
        if response.content_type == 'application/json':
            data = json.loads(response.content)
            self.assertIn('total_reviews', data)
            self.assertIn('average_rating', data)
    
    def test_user_reviews_nonexistent_user(self):
        """Test reviews endpoint with non-existent user"""
        response = self.client.get(
            reverse('user-reviews', kwargs={'user_id': 99999})
        )
        self.assertEqual(response.status_code, 404)

class ReviewIntegrationTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123'
        )
    
    def test_review_workflow(self):
        """Test complete review workflow"""
        # Create review
        review = Review.objects.create(
            reviewer=self.user1,
            reviewed_user=self.user2,
            rating=5,
            comment="Excellent experience!"
        )
        
        # Verify review exists
        self.assertTrue(Review.objects.filter(id=review.id).exists())
        
        # Verify it appears in user's reviews
        user_reviews = Review.objects.filter(reviewed_user=self.user2)
        self.assertEqual(user_reviews.count(), 1)
        self.assertEqual(user_reviews.first().rating, 5)