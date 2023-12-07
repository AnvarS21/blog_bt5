from .models import Like
from post.permissions import IsOwner
from rest_framework import generics, permissions

from .serializers import LikeSerializer


# Create your views here.

class LikeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permission_classes = (IsOwner, )