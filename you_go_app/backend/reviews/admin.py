from django.contrib import admin
'''from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'reviewed_user', 'rating', 'created_at', 'is_active')
    list_filter = ('rating', 'created_at', 'is_active')
    search_fields = ('reviewer__username', 'reviewed_user__username', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Review Information', {
            'fields': ('reviewer', 'reviewed_user', 'rating', 'comment')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('reviewer', 'reviewed_user')
    
    def has_change_permission(self, request, obj=None):
        # Only allow superusers to modify reviews to maintain integrity
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        # Only allow superusers to delete reviews
        return request.user.is_superuser
    
    '''