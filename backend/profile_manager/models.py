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


class UserProfileInfo(models.Model):
    GENDER_CHOICES = (
        ('MALE', 'Homme'),
        ('FEMALE', 'Femme'),
        ('OTHER', 'Autre'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_info')
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='MALE')
    birth_date = models.DateField(null=True, blank=True)
    primary_phone = models.CharField(max_length=30)
    secondary_phone = models.CharField(max_length=30, blank=True, default='')
    professional_summary = models.TextField(blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    district = models.CharField(max_length=100, blank=True, default='')
    neighborhood = models.CharField(max_length=100, blank=True, default='')

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Info: {self.first_name} {self.last_name}"


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=200)  # Poste occupé
    company = models.CharField(max_length=200)  # Structure
    industry = models.CharField(max_length=100)  # Secteur d'activité
    location = models.CharField(max_length=100, blank=True, default='')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)  # Jusqu'à présent
    skills_acquired = models.CharField(max_length=500, blank=True, default='')  # Compétences acquises

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} - {self.company}"


class Certification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=200)  # Libellé du certificat
    year = models.IntegerField()
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True, default='')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, default='')

    pdf_file = models.FileField(upload_to='certifications/pdf/', blank=True, null=True)
    pdf_url = models.URLField(blank=True, default='')  # Google Drive Public URL

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.title} ({self.year})"


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    title = models.CharField(max_length=200)  # Libellé du diplôme
    year = models.IntegerField()
    institution = models.CharField(max_length=200)
    degree_level = models.CharField(max_length=100)  # Niveau d'étude (Bac, Licence, Master, Doctorat...)
    field_of_study = models.CharField(max_length=200, blank=True, default='')  # Spécialité
    location = models.CharField(max_length=100, blank=True, default='')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, default='')
    skills_acquired = models.CharField(max_length=500, blank=True, default='')

    pdf_file = models.FileField(upload_to='educations/pdf/', blank=True, null=True)
    pdf_url = models.URLField(blank=True, default='')  # Google Drive Public URL

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.title} - {self.degree_level} ({self.year})"


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)  # Secteur d'activité
    beneficiary = models.CharField(max_length=200, blank=True, default='')  # Bénéficiaire
    link_url = models.URLField(blank=True, default='')  # Lien d'hébergement
    description = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.industry})"
