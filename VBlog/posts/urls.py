from django.urls import path
from posts.views.views import *

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('my_posts/', MyPostListView.as_view(), name='my_posts'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('<str:slug>/', PostDetailView.as_view(), name='detail'),
    path('<str:slug>/edit/', PostUpdateView.as_view(), name='edit'),
    path('<str:slug>/delete/', PostDeleteView.as_view(), name='delete')
]
