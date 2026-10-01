from django.contrib.auth.models import User
from rest_framework import serializers

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True, required=False)
    phone_number = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'phone_number')
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm') or self.initial_data.get('confirm_password')
        if password_confirm and password != password_confirm:
            raise serializers.ValidationError({"password_confirm": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        phone = validated_data.pop('phone_number', None) or self.initial_data.get('phone')
        username = validated_data.get('username')

        if not username and phone:
            username = phone.strip()

        if not username:
            raise serializers.ValidationError({"username": "Un nom d'utilisateur ou numéro de téléphone est requis."})

        email = validated_data.get('email', '')
        if not email and phone:
            email = f"{phone}@lukamosala.cg"

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
