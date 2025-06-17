# reviews/serializers.py

from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'reviewed_user', 'offer', 'rating', 'comment', 'created_at']
        read_only_fields = ['reviewer', 'created_at']

    def validate(self, data):
        if data['reviewer'] == data['reviewed_user']:
            raise serializers.ValidationError("Vous ne pouvez pas vous évaluer vous-même.")
        return data
