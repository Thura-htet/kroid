from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    editable = serializers.SerializerMethodField(read_only=True)
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Profile
        fields = [
            'username',
            'pen_name',
            'bio',
            'fav_quote',
            'editable',
            'follower_count',
            'following_count',
            'is_following'
        ]
    def get_is_following(self, obj):
        user = self.context.get('user')
        is_following = user in obj.followers.all()
        return is_following
    def get_username(self, obj):
        return obj.user.username
    def get_editable(self, obj):
        return self.context.get('editable')
    # get count for 'follower_count' method field
    def get_follower_count(self, obj):
        return obj.followers.count()
    # get count for 'following_count' method field
    def get_following_count(self, obj):
        return obj.user.following.count()


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'pen_name',
            'bio',
            'fav_quote'
        ]
