from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.db.models import Avg
import logging

from .models import Review

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Review)
def update_reviewed_user_badge(sender, instance, created, **kwargs):
    """
    Update user reliability when a new review is created.
    Also handles review updates if needed.
    """
    try:
        if created:
            logger.info(f"New review created: {instance.reviewer} -> {instance.reviewed_user}")
            
            # Update the reviewed user's reliability
            instance.reviewed_user.update_reliability()
            instance.reviewed_user.save(update_fields=['reliability_score', 'badge'])
            
            # Clear cached statistics
            _clear_user_cache(instance.reviewed_user.id)
            _clear_global_cache()
            
            logger.info(f"Updated reliability for user {instance.reviewed_user.username}")
        
        else:
            # Handle review updates (e.g., rating changes)
            logger.info(f"Review updated: {instance.id}")
            instance.reviewed_user.update_reliability()
            instance.reviewed_user.save(update_fields=['reliability_score', 'badge'])
            _clear_user_cache(instance.reviewed_user.id)
            _clear_global_cache()
            
    except Exception as e:
        logger.error(f"Error updating user reliability: {str(e)}")

@receiver(post_delete, sender=Review)
def handle_review_deletion(sender, instance, **kwargs):
    """
    Update user reliability when a review is deleted.
    """
    try:
        logger.info(f"Review deleted: {instance.reviewer} -> {instance.reviewed_user}")
        
        # Update the reviewed user's reliability after deletion
        instance.reviewed_user.update_reliability()
        instance.reviewed_user.save(update_fields=['reliability_score', 'badge'])
        
        # Clear cached statistics
        _clear_user_cache(instance.reviewed_user.id)
        _clear_global_cache()
        
        logger.info(f"Updated reliability after deletion for user {instance.reviewed_user.username}")
        
    except Exception as e:
        logger.error(f"Error updating user reliability after deletion: {str(e)}")

def _clear_user_cache(user_id):
    """Clear cached data for a specific user"""
    cache_keys = [
        f'user_reviews_{user_id}',
        f'user_rating_avg_{user_id}',
        f'user_review_count_{user_id}',
    ]
    cache.delete_many(cache_keys)

def _clear_global_cache():
    """Clear global cached statistics"""
    cache_keys = [
        'global_review_stats',
        'top_rated_users',
        'recent_reviews',
    ]
    cache.delete_many(cache_keys)

@receiver(post_save, sender=Review)
def update_review_statistics(sender, instance, created, **kwargs):
    """
    Update various review statistics and caches.
    """
    if created:
        try:
            # Update reviewer's review count
            reviewer_review_count = Review.objects.filter(reviewer=instance.reviewer).count()
            
            # You might want to store this on the user model or in cache
            cache.set(f'reviewer_count_{instance.reviewer.id}', reviewer_review_count, 3600)
            
            # Update reviewed user's average rating
            avg_rating = Review.objects.filter(
                reviewed_user=instance.reviewed_user,
                is_active=True
            ).aggregate(avg_rating=Avg('rating'))['avg_rating']
            
            if avg_rating:
                cache.set(f'user_rating_avg_{instance.reviewed_user.id}', avg_rating, 3600)
            
        except Exception as e:
            logger.error(f"Error updating review statistics: {str(e)}")

# Optional: Signal for handling bulk operations
def bulk_update_user_reliability(user_ids):
    """
    Utility function to bulk update reliability for multiple users.
    Useful for data migrations or admin operations.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    users = User.objects.filter(id__in=user_ids)
    for user in users:
        try:
            user.update_reliability()
            user.save(update_fields=['reliability_score', 'badge'])
            _clear_user_cache(user.id)
        except Exception as e:
            logger.error(f"Error bulk updating reliability for user {user.id}: {str(e)}")
    
    _clear_global_cache()