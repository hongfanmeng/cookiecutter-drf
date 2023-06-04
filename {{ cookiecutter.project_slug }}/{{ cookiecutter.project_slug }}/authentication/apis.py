from django.conf import settings
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebTokenView

from {{ cookiecutter.project_slug }}.api.mixins import ApiAuthMixin
from {{ cookiecutter.project_slug }}.authentication.services import auth_logout
from {{ cookiecutter.project_slug }}.users.models import BaseUser


class UserJwtLoginApi(ObtainJSONWebTokenView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            response.status_code = status.HTTP_200_OK

        return response


class UserJwtLogoutApi(ApiAuthMixin, APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # try to logout, user might provide invalid token
        try:
            auth_logout(request.user)
        except Exception:
            pass

        response = Response()

        # delete cookie even if logout failed
        if settings.JWT_AUTH["JWT_AUTH_COOKIE"] is not None:
            response.delete_cookie(settings.JWT_AUTH["JWT_AUTH_COOKIE"])

        return response


class UserMeApi(ApiAuthMixin, GenericAPIView, RetrieveModelMixin):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ("id", "email", "is_admin")

    serializer_class = OutputSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
