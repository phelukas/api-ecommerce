from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.serializers import UserSerializer, AddUserSerializer
from django.http import Http404


class UserView(APIView):
    """
    CRUD user
    """

    def edit(self, request, pk, partial=False):
        is_superuser = self.is_superuser(request)

        if pk and not is_superuser:
            raise Http404

        if pk:
            self.check_pk_none(pk)
            user = User.objects.get(pk=pk)
            data, status_ = self.edit_serializer(
                request, user, partial=partial)

        usuario = request.user
        data, status_ = self.edit_serializer(request, usuario, partial=partial)

        return data, status_

    def edit_serializer(self, request, user, partial=False):
        serializer = AddUserSerializer(
            user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        status_ = status.HTTP_200_OK

        return data, status_

    def check_pk_none(self, pk):
        usuario = User.objects.filter(pk=pk)

        if len(usuario) == 0:

            msg = f'Usuario com id {pk} não encontrado'
            status_ = status.HTTP_404_NOT_FOUND
            return Response({"error": msg}, status=status_)

        return False

    def is_superuser(self, request):
        try:
            is_superuser = request.user.is_superuser
        except:
            is_superuser = False

        return is_superuser

    def get(self, request, pk=None):
        is_superuser = self.is_superuser(request)

        if not is_superuser:
            instance = request.user
            serializer = UserSerializer(instance)

        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = AddUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None, format=None):
        data, status_ = self.edit(request, pk)
        return Response(data, status=status_)

    def patch(self, request, pk, format=None):
        data, status_ = self.edit(request, pk, partial=True)
        return Response(data, status=status_)
