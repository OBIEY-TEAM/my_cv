from django.db import models
from django.contrib.auth.models import User

class JobOffer(models.Model):
    SOURCE_TYPES = (
        ('URL', 'Lien URL'),
        ('PDF', 'Fichier PDF'),
        ('TEXT', 'Texte Brut'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_offers')
    source_type = models.CharField(max_length=10, choices=SOURCE_TYPES, default='TEXT')
    source_url = models.URLField(blank=True, null=True)
    source_file = models.FileField(upload_to='jobs/sources/', blank=True, null=True)
    raw_text = models.TextField(blank=True, default='')

    title = models.CharField(max_length=255, blank=True, default='')
    company = models.CharField(max_length=255, blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='')
    site_category = models.CharField(max_length=100, blank=True, default='acpe')
    abbreviation = models.CharField(max_length=100, blank=True, default='POSTE')
    cleaned_description = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} @ {self.company}" if self.title else f"JobOffer #{self.id}"

class ApplicationPackage(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('approuved', 'Approuvé'),
        ('pending', 'En attente'),
        ('failed', 'Échoué'),
    )
    PROCESSING_STATUS_CHOICES = (
        ('finalized', 'Finalisé'),
        ('pending', 'En attente'),
        ('inprocess', 'En traitement'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='application_packages')
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name='packages')

    cv_pdf = models.FileField(upload_to='applications/cv/', blank=True, null=True)
    cover_letter_pdf = models.FileField(upload_to='applications/lm/', blank=True, null=True)
    email_txt = models.FileField(upload_to='applications/email/', blank=True, null=True)
    offer_pdf = models.FileField(upload_to='applications/offer/', blank=True, null=True)
    zip_package = models.FileField(upload_to='applications/zip/', blank=True, null=True)

    email_subject = models.CharField(max_length=255, blank=True, default='')
    email_body = models.TextField(blank=True, default='')

    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='approuved')
    processing_status = models.CharField(max_length=20, choices=PROCESSING_STATUS_CHOICES, default='finalized')

    folder_path = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Package for {self.job_offer.title} - {self.user.username}"
