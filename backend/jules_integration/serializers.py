from rest_framework import serializers
from .models import JulesSession, JulesActivity

class JulesActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = JulesActivity
        fields = ['id', 'session', 'activity_id', 'activity_type', 'content', 'plan_approved', 'created_at']
        read_only_fields = ['id', 'created_at']

class JulesSessionSerializer(serializers.ModelSerializer):
    activities = JulesActivitySerializer(many=True, read_only=True)

    class Meta:
        model = JulesSession
        fields = ['id', 'user', 'session_id', 'prompt_used', 'status', 'created_at', 'updated_at', 'activities']
        read_only_fields = ['id', 'created_at', 'updated_at', 'activities']
