# reviews/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReviewCreateView, 
    ReviewListView, 
    GlobalUserStatsView,
    ReviewDetailView,
    UserReviewStatsView,
    TopRatedUsersView,
    UserReviewSummaryView
)

# REST API router for ViewSet


app_name = 'reviews'

urlpatterns = [
    # Basic CRUD operations
    path('', ReviewCreateView.as_view(), name='create-review'),
    path('<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    
    # User-specific endpoints
    path('user/<int:user_id>/', ReviewListView.as_view(), name='user-reviews'),
    path('user/<int:user_id>/stats/', UserReviewStatsView.as_view(), name='user-review-stats'),
    path('user/<int:user_id>/summary/', UserReviewSummaryView.as_view(), name='user-review-summary'),
    
    # Statistics and analytics
    path('stats/', GlobalUserStatsView.as_view(), name='global-user-stats'),
    path('stats/top-users/', TopRatedUsersView.as_view(), name='top-rated-users'),
 

]
'''
# Additional URL patterns for specific use cases
additional_patterns = [
    # Admin/moderation endpoints
    path('admin/pending/', 'reviews.views.PendingReviewsView', name='pending-reviews'),
    path('admin/flagged/', 'reviews.views.FlaggedReviewsView', name='flagged-reviews'),
    
    # Bulk operations
    path('bulk/approve/', 'reviews.views.BulkApproveView', name='bulk-approve-reviews'),
    path('bulk/delete/', 'reviews.views.BulkDeleteView', name='bulk-delete-reviews'),
    
    # Export functionality
    path('export/csv/', 'reviews.views.ExportReviewsCSV', name='export-reviews-csv'),
    path('export/user/<int:user_id>/csv/', 'reviews.views.ExportUserReviewsCSV', name='export-user-reviews-csv'),
    
    # Review interactions
    path('<int:review_id>/flag/', 'reviews.views.FlagReviewView', name='flag-review'),
    path('<int:review_id>/helpful/', 'reviews.views.MarkHelpfulView', name='mark-helpful'),
    
    # Search and filtering
    path('search/', 'reviews.views.ReviewSearchView', name='search-reviews'),
    path('filter/', 'reviews.views.ReviewFilterView', name='filter-reviews'),
]

# Uncomment to include additional patterns if needed
# urlpatterns += additional_patterns
'''