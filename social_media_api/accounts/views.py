from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated



class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


from django.shortcuts import get_object_or_404
from .models import CustomUser

class FollowUserView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, username):
        try:
            user_to_follow = CustomUser.objects.get(username=username)
            request.user.following.add(user_to_follow)
            return Response({"message": f"You are now following {username}."})
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

class UnfollowUserView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, username):
        try:
            user_to_unfollow = CustomUser.objects.get(username=username)
            request.user.following.remove(user_to_unfollow)
            return Response({"message": f"You have unfollowed {username}."})
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=404)