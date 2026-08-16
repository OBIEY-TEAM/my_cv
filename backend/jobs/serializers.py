from rest_framework import serializers
from .models import JobOffer, ApplicationPackage

class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class ApplicationPackageSerializer(serializers.ModelSerializer):
    job_offer = JobOfferSerializer(read_only=True)

    class Meta:
        model = ApplicationPackage
        fields = '__all__'
        read_only_fields = ('user', 'created_at')
