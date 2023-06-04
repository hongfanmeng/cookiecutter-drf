from django_filters import rest_framework as filters
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import LimitOffsetPagination

from {{ cookiecutter.project_slug }}.users.models import BaseUser


# TODO: When JWT is resolved, add authenticated version
class UserListApi(GenericAPIView, ListModelMixin):
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("id", "is_admin", "email")
    queryset = BaseUser.objects.all()

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ("id", "email", "is_admin")

    serializer_class = OutputSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
