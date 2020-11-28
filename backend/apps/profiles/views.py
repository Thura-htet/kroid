from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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
        data = {
            'username': profile.user.username,
            'pen_name': profile.pen_name,
            'bio': profile.bio,
            'fav_quote': profile.fav_quote,
            'editable': editable
        }
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "PUT":
        serializer = ProfileUpdateSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.update(instance=profile, validated_data=serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
