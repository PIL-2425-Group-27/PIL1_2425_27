# reviews/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Review, ReviewFlag, UserReviewSummary

User = get_user_model()

class ReviewerSerializer(serializers.ModelSerializer):
    """Minimal serializer for reviewer information"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name']

class ReviewedUserSerializer(serializers.ModelSerializer):
    """Minimal serializer for reviewed user information"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name']

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_info = ReviewerSerializer(source='reviewer', read_only=True)
    reviewed_user_info = ReviewedUserSerializer(source='reviewed_user', read_only=True)
    average_detailed_rating = serializers.ReadOnlyField()
    
    class Meta:
        model = Review
        fields = [
            'id', 'reviewer', 'reviewed_user', 'offer', 'rating', 
            'punctuality_rating', 'communication_rating', 'vehicle_condition_rating',
            'comment', 'review_type', 'created_at', 'updated_at',
            'reviewer_info', 'reviewed_user_info', 'average_detailed_rating',
            'is_verified'
        ]
        read_only_fields = ['reviewer', 'created_at', 'updated_at', 'is_verified']

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            # Prevent self-review
            if request.user == data.get('reviewed_user'):
                raise serializers.ValidationError("You cannot review yourself.")
            
            # Check if review already exists
            if Review.objects.filter(
                reviewer=request.user,
                reviewed_user=data.get('reviewed_user'),
                offer=data.get('offer')
            ).exists():
                raise serializers.ValidationError("You have already reviewed this user for this ride.")
        
        # Validate vehicle condition rating for passenger reviews
        if data.get('review_type') == 'PASSENGER' and data.get('vehicle_condition_rating'):
            raise serializers.ValidationError("Vehicle condition rating only applies to driver reviews.")
        
        return data

    def create(self, validated_data):
        # Set reviewer from request user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['reviewer'] = request.user
        
        return super().create(validated_data)

class ReviewCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating reviews"""
    class Meta:
        model = Review
        fields = [
            'reviewed_user', 'offer', 'rating', 
            'punctuality_rating', 'communication_rating', 'vehicle_condition_rating',
            'comment', 'review_type'
        ]

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            # Prevent self-review
            if request.user == data.get('reviewed_user'):
                raise serializers.ValidationError("You cannot review yourself.")
            
            # Check if review already exists
            if Review.objects.filter(
                reviewer=request.user,
                reviewed_user=data.get('reviewed_user'),
                offer=data.get('offer')
            ).exists():
                raise serializers.ValidationError("You have already reviewed this user for this ride.")
        
        return data

class ReviewListSerializer(serializers.ModelSerializer):
    """Serializer for listing reviews with minimal data"""
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)
    reviewer_first_name = serializers.CharField(source='reviewer.first_name', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'rating', 'comment', 'review_type', 'created_at',
            'reviewer_name', 'reviewer_first_name', 'is_verified',
            'punctuality_rating', 'communication_rating', 'vehicle_condition_rating'
        ]

class ReviewFlagSerializer(serializers.ModelSerializer):
    flagger_name = serializers.CharField(source='flagger.username', read_only=True)
    
    class Meta:
        model = ReviewFlag
        fields = ['id', 'review', 'reason', 'description', 'created_at', 'flagger_name']
        read_only_fields = ['flagger', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['flagger'] = request.user
        return super().create(validated_data)

class UserReviewSummarySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    # Rating distribution as percentages
    rating_distribution = serializers.SerializerMethodField()
    
    class Meta:
        model = UserReviewSummary
        fields = [
            'username', 'total_reviews', 'average_rating',
            'avg_punctuality', 'avg_communication', 'avg_vehicle_condition',
            'rating_distribution', 'last_updated'
        ]
    
    def get_rating_distribution(self, obj):
        if obj.total_reviews == 0:
            return {}
        
        return {
            '5_stars': round((obj.five_star_count / obj.total_reviews) * 100, 1),
            '4_stars': round((obj.four_star_count / obj.total_reviews) * 100, 1),
            '3_stars': round((obj.three_star_count / obj.total_reviews) * 100, 1),
            '2_stars': round((obj.two_star_count / obj.total_reviews) * 100, 1),
            '1_star': round((obj.one_star_count / obj.total_reviews) * 100, 1),
        }

class UserReviewStatsSerializer(serializers.Serializer):
    """Serializer for user review statistics"""
    total_reviews_given = serializers.IntegerField()
    total_reviews_received = serializers.IntegerField()
    average_rating_received = serializers.DecimalField(max_digits=3, decimal_places=2)
    average_rating_given = serializers.DecimalField(max_digits=3, decimal_places=2)
    recent_reviews = ReviewListSerializer(many=True)
    review_summary = UserReviewSummarySerializer()