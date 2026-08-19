from django.db import models
from django.conf import settings


class JulesSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jules_sessions",
        null=True,
        blank=True,
    )
    session_id = models.CharField(max_length=255, unique=True, help_text="Jules API session name/ID")
    prompt_used = models.TextField(blank=True, default="")
    status = models.CharField(max_length=50, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"JulesSession({self.session_id}) - {self.status}"


class JulesActivity(models.Model):
    session = models.ForeignKey(
        JulesSession,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    activity_id = models.CharField(max_length=255, blank=True, default="")
    activity_type = models.CharField(max_length=50, help_text="e.g. plan_generated, message, error")
    content = models.JSONField(default=dict, blank=True)
    plan_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"JulesActivity({self.activity_type}) for Session({self.session.session_id})"
