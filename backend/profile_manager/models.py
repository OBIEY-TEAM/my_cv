from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=255, blank=True, default="Consultant IT & Expert Fullstack")
    phone = models.CharField(max_length=50, blank=True, default="+242 06 613 01 18")
    cities = models.CharField(max_length=255, blank=True, default="Brazzaville & Pointe-Noire, Congo")
    github_url = models.URLField(blank=True, default="https://github.com")
    linkedin_url = models.URLField(blank=True, default="https://linkedin.com")

    readme_content = models.TextField(blank=True, default="")

    original_photo = models.ImageField(upload_to='profiles/original/', blank=True, null=True)
    cropped_photo = models.ImageField(upload_to='profiles/cropped/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
