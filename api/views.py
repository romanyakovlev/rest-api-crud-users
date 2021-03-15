from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import ReadOnlyUserSerializer, WriteOnlyUserSerializer
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.authentication import TokenAuthentication


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [TokenAuthentication]
    serializer_classes = {
        'list': ReadOnlyUserSerializer,
        'create': WriteOnlyUserSerializer,
        'retrieve': ReadOnlyUserSerializer,
        'update': WriteOnlyUserSerializer,
        'partial_update': WriteOnlyUserSerializer,
        'destroy': WriteOnlyUserSerializer,
    }
    default_serializer_class = ReadOnlyUserSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)
