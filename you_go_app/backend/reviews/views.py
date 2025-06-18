# reviews/views.py

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Q
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db import transaction

from .models import Review, ReviewFlag, UserReviewSummary
from .serializers import (
    ReviewSerializer, ReviewCreateSerializer, ReviewListSerializer,
    ReviewFlagSerializer, UserReviewSummarySerializer, UserReviewStatsSerializer
)
from offers.models import RideOffer, RideRequest

User = get_user_model()

class ReviewCreateView(generics.CreateAPIView):
    """Create a new review"""
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        with transaction.atomic():
            review = serializer.save(reviewer=self.request.user)
            
            # Update or create user review summary
            summary, created = UserReviewSummary.objects.get_or_create(
                user=review.reviewed_user
            )
            summary.update_summary()

class ReviewListView(generics.ListAPIView):
    """List reviews for a specific user"""
    serializer_class = ReviewListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        review_type = self.request.query_params.get('type', None)
        
        queryset = Review.objects.filter(reviewed_user__id=user_id)
        
        if review_type:
            queryset = queryset.filter(review_type=review_type.upper())
        
        return queryset.select_related('reviewer').order_by('-created_at')

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a specific review"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)

    def perform_update(self, serializer):
        with transaction.atomic():
            review = serializer.save()
            # Update summary when review is modified
            summary, created = UserReviewSummary.objects.get_or_create(
                user=review.reviewed_user
            )
            summary.update_summary()

    def perform_destroy(self, instance):
        with transaction.atomic():
            reviewed_user = instance.reviewed_user
            super().perform_destroy(instance)
            # Update summary when review is deleted
            summary, created = UserReviewSummary.objects.get_or_create(
                user=reviewed_user
            )
            summary.update_summary()

class ReviewFlagView(generics.CreateAPIView):
    """Flag a review for moderation"""
    serializer_class = ReviewFlagSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(flagger=self.request.user)

class UserReviewSummaryView(generics.RetrieveAPIView):
    """Get user review summary"""
    serializer_class = UserReviewSummarySerializer
    permission_classes = [AllowAny]
    lookup_field = 'user_id'

    def get_object(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        
        summary, created = UserReviewSummary.objects.get_or_create(user=user)
        if created or (now() - summary.last_updated).days > 1:
            # Update summary if it's new or older than 1 day
            summary.update_summary()
        
        return summary

class UserReviewStatsView(APIView):
    """Get comprehensive review statistics for a user"""
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        # Get or create summary
        summary, created = UserReviewSummary.objects.get_or_create(user=user)
        if created or (now() - summary.last_updated).days > 1:
            summary.update_summary()
        
        # Get recent reviews (last 10)
        recent_reviews = Review.objects.filter(
            reviewed_user=user
        ).select_related('reviewer').order_by('-created_at')[:10]
        
        # Calculate additional stats
        reviews_given = Review.objects.filter(reviewer=user)
        
        stats = {
            'total_reviews_given': reviews_given.count(),
            'total_reviews_received': summary.total_reviews,
            'average_rating_received': float(summary.average_rating),
            'average_rating_given': float(reviews_given.aggregate(
                avg=Avg('rating')
            )['avg'] or 0),
            'recent_reviews': ReviewListSerializer(recent_reviews, many=True).data,
            'review_summary': UserReviewSummarySerializer(summary).data
        }
        
        return Response(stats)

class GlobalUserStatsView(APIView):
    """Get global user statistics including rides and reviews"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = now().date()

        # Get last 7 days
        week_dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
        labels = [date.strftime('%A') for date in week_dates]

        trajet_counts = []
        km_by_day = []
        reviews_by_day = []

        for date in week_dates:
            # Count rides for this day
            demandes = RideRequest.objects.filter(
                passenger=user, 
                status='ACCEPTEE', 
                date_trajet=date
            )
            offres = RideOffer.objects.filter(
                driver=user, 
                status='ACTIF', 
                date_trajet=date
            )

            total_trajets = demandes.count() + offres.count()
            trajet_counts.append(total_trajets)

            # Estimate distance (3 km per ride average)
            km = total_trajets * 3
            km_by_day.append(float(km))
            
            # Count reviews given this day
            reviews_count = Review.objects.filter(
                reviewer=user,
                created_at__date=date
            ).count()
            reviews_by_day.append(reviews_count)

        # Get user's review summary
        summary, created = UserReviewSummary.objects.get_or_create(user=user)
        if created:
            summary.update_summary()

        return Response({
            "labels": labels,
            "total_trajets": trajet_counts,
            "total_km": km_by_day,
            "reviews_given": reviews_by_day,
            "user_rating": float(summary.average_rating),
            "total_reviews_received": summary.total_reviews,
        })

class TopRatedUsersView(APIView):
    """Get top-rated users"""
    permission_classes = [AllowAny]

    def get(self, request):
        # Get top 10 users with highest ratings (minimum 5 reviews)
        top_users = UserReviewSummary.objects.filter(
            total_reviews__gte=5
        ).order_by('-average_rating')[:10]
        
        data = []
        for summary in top_users:
            data.append({
                'user_id': summary.user.id,
                'username': summary.user.username,
                'average_rating': float(summary.average_rating),
                'total_reviews': summary.total_reviews,
                'avg_punctuality': float(summary.avg_punctuality) if summary.avg_punctuality else None,
                'avg_communication': float(summary.avg_communication) if summary.avg_communication else None,
            })
        
        return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_update_summaries(request):
    """Admin endpoint to update all user review summaries"""
    if not request.user.is_staff:
        return Response(
            {'error': 'Permission denied'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    summaries = UserReviewSummary.objects.all()
    updated_count = 0
    
    for summary in summaries:
        summary.update_summary()
        updated_count += 1
    
    return Response({
        'message': f'Updated {updated_count} user review summaries'
    })

class ReviewAnalyticsView(APIView):
    """Get review analytics for the platform"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Overall platform statistics
        total_reviews = Review.objects.count()
        avg_platform_rating = Review.objects.aggregate(
            avg=Avg('rating')
        )['avg'] or 0
        
        # Rating distribution
        rating_dist = Review.objects.values('rating').annotate(
            count=Count('rating')
        ).order_by('rating')
        
        # Reviews by type
        type_dist = Review.objects.values('review_type').annotate(
            count=Count('review_type')
        )
        
        # Recent activity (last 30 days)
        thirty_days_ago = now() - timedelta(days=30)
        recent_reviews = Review.objects.filter(
            created_at__gte=thirty_days_ago
        ).count()
        
        # Flagged reviews
        flagged_reviews = Review.objects.filter(is_flagged=True).count()
        
        return Response({
            'total_reviews': total_reviews,
            'average_rating': round(float(avg_platform_rating), 2),
            'rating_distribution': list(rating_dist),
            'type_distribution': list(type_dist),
            'recent_reviews_30d': recent_reviews,
            'flagged_reviews': flagged_reviews,
        })