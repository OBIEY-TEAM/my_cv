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
    last_name = models.CharField(max_length=100)  # Nom
    first_name = models.CharField(max_length=100)  # Prénom
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='MALE')  # Genre
    birth_date = models.DateField(null=True, blank=True)  # Date de naissance
    primary_phone = models.CharField(max_length=30)  # Numéro principal
    secondary_phone = models.CharField(max_length=30, blank=True, default='')  # Numéro secondaire
    professional_summary = models.TextField(blank=True, default='')  # Résumé professionnel
    address = models.CharField(max_length=255, blank=True, default='')  # Adresse / adressepay
    adressepay = models.CharField(max_length=255, blank=True, default='')  # Champ alias adressepay
    district = models.CharField(max_length=100, blank=True, default='')  # Arrondissement
    neighborhood = models.CharField(max_length=100, blank=True, default='')  # Quartier

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Info: {self.first_name} {self.last_name}"


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=200)  # Poste occupé
    company = models.CharField(max_length=200)  # Structure
    industry = models.CharField(max_length=100)  # Secteur d'activité
    location = models.CharField(max_length=100, blank=True, default='')  # Lieu
    start_date = models.DateField()  # Date de début
    end_date = models.DateField(null=True, blank=True)  # Date de fin
    is_current = models.BooleanField(default=False)  # Jusqu'à présent
    skills_acquired = models.CharField(max_length=500, blank=True, default='')  # Compétences acquises

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} - {self.company}"


class Certification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=200)  # Libellé certificat
    year = models.IntegerField()  # Année
    institution = models.CharField(max_length=200)  # Institution
    location = models.CharField(max_length=100, blank=True, default='')  # Lieu
    start_date = models.DateField(null=True, blank=True)  # Date de début
    end_date = models.DateField(null=True, blank=True)  # Date de fin
    description = models.TextField(blank=True, default='')  # Description

    pdf_file = models.FileField(upload_to='certifications/pdf/', blank=True, null=True)
    pdf_url = models.URLField(blank=True, default='')  # En pdf (Google Drive Public URL)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.title} ({self.year})"


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    title = models.CharField(max_length=200)  # Libellé du diplôme
    year = models.IntegerField()  # Année
    institution = models.CharField(max_length=200)  # Institution
    degree_level = models.CharField(max_length=100)  # Niveau d'étude
    field_of_study = models.CharField(max_length=200, blank=True, default='')  # Spécialité
    location = models.CharField(max_length=100, blank=True, default='')  # Lieu
    start_date = models.DateField(null=True, blank=True)  # Date de début
    end_date = models.DateField(null=True, blank=True)  # Date de fin
    description = models.TextField(blank=True, default='')
    skills_acquired = models.CharField(max_length=500, blank=True, default='')  # Compétences acquises

    pdf_file = models.FileField(upload_to='educations/pdf/', blank=True, null=True)
    pdf_url = models.URLField(blank=True, default='')  # Diplôme en pdf (Google Drive Public URL)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.title} - {self.degree_level} ({self.year})"


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=200)  # Nom du projet
    industry = models.CharField(max_length=100)  # Secteur d'activité
    beneficiary = models.CharField(max_length=200, blank=True, default='')  # Bénéficiaire
    link_url = models.URLField(blank=True, default='')  # Lien d'hébergement
    description = models.TextField(blank=True, default='')  # Description

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.industry})"
