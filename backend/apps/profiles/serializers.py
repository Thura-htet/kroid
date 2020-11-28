from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    editable = serializers.BooleanField()
    class Meta:
        model = Profile
        fields = [
            'username',
            'pen_name',
            'bio',
            'fav_quote',
            'editable'
        ]

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'pen_name',
            'bio',
            'fav_quote'
        ]
