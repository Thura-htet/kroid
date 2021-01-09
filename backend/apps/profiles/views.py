from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from ..posts.models import Post
from .models import Profile
from ..posts.serializers import ListedPostSerializer
from .serializers import ProfileSerializer, ProfileUpdateSerializer


@api_view(['GET', 'PUT'])
def profile_view(request, username, *args, **kwargs):
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        editable = False
        if request.user.username == profile.user.username:
            editable = True
        serializer = ProfileSerializer(profile, context={'editable':editable, 'user': request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = ProfileUpdateSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.update(instance=profile, validated_data=serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_follow_view(request, username, *args, **kwargs):
    object_user = request.user
    try:
        subject_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    subject_profile = subject_user.profile
    action = request.data.get('action') or None
    if action == 'follow':
        subject_profile.followers.add(object_user)
        return Response({'message': 'Followed author'}, status=status.HTTP_200_OK)
    elif action == 'unfollow':
        subject_profile.followers.remove(object_user)
        return Response({'message': 'Unfollowed author'}, status=status.HTTP_200_OK)
    else:
        pass
