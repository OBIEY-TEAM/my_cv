from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Profile
from .serializers import ProfileSerializer

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

class PhotoCropView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)

        if 'photo' in request.FILES:
            photo_file = request.FILES['photo']
            profile.original_photo = photo_file
            profile.save()
            img = Image.open(photo_file)
        elif profile.original_photo:
            img = Image.open(profile.original_photo.path)
        else:
            return Response({"error": "Aucune photo fournie ou enregistrée."}, status=status.HTTP_400_BAD_REQUEST)

        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2

        img_cropped = img.crop((left, top, right, bottom))
        img_cropped = img_cropped.resize((600, 600), Image.Resampling.LANCZOS)

        buffer = BytesIO()
        img_cropped.save(buffer, format='PNG')
        file_name = f"profile_cropped_{request.user.id}.png"

        profile.cropped_photo.save(file_name, ContentFile(buffer.getvalue()), save=True)

        return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)
