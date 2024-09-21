from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserViewSet, accounts_home

# Create a router and register the UserViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', accounts_home, name='accounts-home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('', include(router.urls)),  # Include the router URLs for user management
    path('follow/<int:user_id>/', UserViewSet.as_view({'post': 'follow_user'}), name='follow-user'),
    path('unfollow/<int:user_id>//', UserViewSet.as_view({'post': 'unfollow_user'}), name='unfollow-user'),
]
