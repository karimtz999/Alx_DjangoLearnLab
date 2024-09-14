from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    home,
    post_list,
    register,
    login_view,
    logout_view,
    profile,
    edit_profile
)

urlpatterns = [
    path('', home, name='home'),
    path('posts/', PostListView.as_view(), name='post-list'),  # Post list view
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # Post detail view
    path('posts/new/', PostCreateView.as_view(), name='post-create'),  # Post create view
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),  # Post update view
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # Post delete view
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
]
