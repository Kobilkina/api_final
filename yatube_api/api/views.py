from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters

from posts.models import Group, Post, Comment, Follow

from .serializers import GroupSerializer, FollowSerializer
from .serializers import PostSerializer, CommentSerializer

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.get_object().author == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied('dont touch')

    def destroy(self, request, pk=None, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super(PostViewSet, self).destroy(request, pk, *args, **kwargs)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        return self.get_post().comments.all().select_related('author', 'post')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())

    def perform_update(self, serializer):
        if self.get_object().author == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied('dont touch')

    def destroy(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super(CommentViewSet, self).destroy(request, *args, **kwargs)


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('following',)

    def get_following(self):
        following = self.kwargs.get('following')
        return get_object_or_404(User, username=following)

    def get_queryset(self):
        return self.request.user.following.all()

    def perform_create(self, serializer):
        if self.request.user == self.get_following():
            raise PermissionDenied('cant follow yourself')
        serializer.save(user=self.request.user, following=self.get_following())


    #def get_queryset(self):
    #    search = self.kwargs['search']
    #    if search:
    #        return self.queryset.filter(following=search, user=self.request.user)
    #    return self.queryset.filter(user=self.request.user)