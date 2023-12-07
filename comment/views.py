from rest_framework import generics, permissions
from post.permissions import CommentsPermission

from .models import Comment
from . import serializers


class CommentCreateViews(generics.CreateAPIView):
    serializer_class = serializers.CommentSerializers
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializers

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [CommentsPermission(), ]
        return [permissions.AllowAny(), ]


class UserCommentsView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.CommentSerializers

    def get_queryset(self):
        return Comment.objects.filter(owner=self.request.user.id)






