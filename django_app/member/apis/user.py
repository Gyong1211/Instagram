from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.permissions import ObjectIsRequestUser
from ..models import User
from ..serializers.user import *

__all__ = (
    'UserRetrieveUpdateDestroyView',
    'UserListCreateView'
)


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser,
    )


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserCreationSerializer
