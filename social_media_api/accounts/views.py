from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, PostSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from .models import Post
from django.http import HttpResponse

User = get_user_model()

def accounts_home(request):
    return HttpResponse("Welcome to the accounts home page!")
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # List all users
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, pk=None):
        # Retrieve a specific user profile
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def follow_user(self, request, pk=None):
        # Follow a user
        user_to_follow = get_object_or_404(CustomUser, pk=pk)
        request.user.following.add(user_to_follow)
        return Response({"message": f"You are now following {user_to_follow.username}."})

    def unfollow_user(self, request, pk=None):
        # Unfollow a user
        user_to_unfollow = get_object_or_404(CustomUser, pk=pk)
        request.user.following.remove(user_to_unfollow)
        return Response({"message": f"You have unfollowed {user_to_unfollow.username}."})
    
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    if request.user == user_to_follow:
        return Response({'error': "You can't follow yourself"}, status=status.HTTP_400_BAD_REQUEST)
    
    request.user.following.add(user_to_follow)
    return Response({'success': f'You are now following {user_to_follow.username}'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
    request.user.following.remove(user_to_unfollow)
    return Response({'success': f'You have unfollowed {user_to_unfollow.username}'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    # Get the users that the current user is following
    following_users = request.user.following.all()

    # Get the posts from the followed users, ordered by creation date
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

    # You may want to serialize the posts (assuming you have a PostSerializer)
    serialized_posts = PostSerializer(posts, many=True)

    return Response(serialized_posts.data, status=status.HTTP_200_OK)