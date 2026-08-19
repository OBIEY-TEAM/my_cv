from rest_framework import serializers
from .models import JobOffer, ApplicationPackage

class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class ApplicationPackageSerializer(serializers.ModelSerializer):
    job_offer = JobOfferSerializer(read_only=True)
    cv_pdf = serializers.SerializerMethodField()
    cover_letter_pdf = serializers.SerializerMethodField()
    email_txt = serializers.SerializerMethodField()
    offer_pdf = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationPackage
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

    def _get_file_url(self, obj, field_name):
        val = getattr(obj, field_name, None)
        if not val:
            return ""
        if isinstance(val, str):
            return val
        return getattr(val, 'url', str(val))

    def get_cv_pdf(self, obj):
        return self._get_file_url(obj, 'cv_pdf')

    def get_cover_letter_pdf(self, obj):
        return self._get_file_url(obj, 'cover_letter_pdf')

    def get_email_txt(self, obj):
        return self._get_file_url(obj, 'email_txt')

    def get_offer_pdf(self, obj):
        return self._get_file_url(obj, 'offer_pdf')
