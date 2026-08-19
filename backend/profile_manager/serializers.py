from rest_framework import serializers
from .models import Profile, UserProfileInfo, Experience, Certification, Education, Project

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Profile
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'title', 'phone', 'cities', 'github_url', 'linkedin_url',
            'readme_content', 'original_photo', 'cropped_photo',
            'created_at', 'updated_at'
        )


class UserProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileInfo
        fields = '__all__'
        read_only_fields = ('user',)


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
        read_only_fields = ('user',)


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'
        read_only_fields = ('user',)


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ('user',)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('user',)
