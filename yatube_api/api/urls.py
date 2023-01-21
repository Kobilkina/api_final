from django.urls import path, include
from rest_framework import routers

from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('groups', GroupViewSet, basename='group')
router_v1.register(r'posts/(?P<post_id>\d+)/comments',
                   CommentViewSet, basename='comment')
router_v1.register('follow', FollowViewSet, basename='follow')

jwt_patterns = [path('', include('djoser.urls.jwt'))]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(jwt_patterns)),
]
