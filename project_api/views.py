from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from project_api.schemas import ProfileSchema

# from utils.base_schemas import metadata_paginator
from utils.paginator import s_paginator

from project_api.serializers import UserProfileSerializer, HelloSerializer
from project_api import models


class HelloAPIView(APIView):
    """Test API View"""
    seriallizer_class = HelloSerializer

    def get(self, request, format=None):
        an_apis = ['quyen', 'ca', 'ne']
        #  mac dinh response tra ve http 200
        return Response({'message': 'Hello!', 'an-apis': an_apis})

    def post(self, request):

        serializer = self.seriallizer_class(data=request.data)

        if serializer.is_valid():
            # lay ra thuoc tinh  ( tuong tu astributes trong nodjs)
            name = serializer.validated_data.get('name')
            message = f'hello {name}'
            return Response({'message': message})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Handle deleting an object"""
        return Response({'method': 'DELETE'})


class HelloViewSets(viewsets.ViewSet):
    """Test APi ViewSets"""
    serializer_class = HelloSerializer

    def list(self, request):
        """Return a hello message"""
        a_viewset = [{"id": 1, "name": "quyen"}, {"id": 2, "name": "VU"}]
        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle getting an obj by ID"""
        return Response({'method': 'GET'})

    def update(self, request, pk=None):
        return Response({'method': 'PUT'})

    def partial_update(self, request, pk=None):
        return Response({'method': 'PATCH'})

    def destroy(self, request, pk=None):
        return Response({'method': 'DELETE'})


class UserProfileViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                         mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Handle creating and updating profile"""
    permission_classes = [AllowAny]
    serializer_class = UserProfileSerializer

    search_fields = ['name', 'email']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = (AllowAny, )
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(
        operation_summary='Danh sách danh mục sản phẩm',
        manual_parameters=[
            openapi.Parameter(
                'parent_id',
                type=openapi.TYPE_INTEGER,
                in_=openapi.IN_QUERY,
                description=
                'ID của một category => sử dụng param này để lấy các category con của một category'
            )
        ],
        responses={
            200:
            openapi.Response(description='Success',
                             schema=openapi.Schema(
                                 type=openapi.TYPE_ARRAY,
                                 items=ProfileSchema.get_output()))
        })
    def list(self, request):
        try:
            search = request.GET.get('search')
            queryset = models.UserProfile.objects.all()
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) | Q(email__icontains=search))
            data, metadata = s_paginator(queryset, request, True)
            serializer = self.get_serializer(data,
                                             many=True,
                                             context={
                                                 'request': request
                                             }).data
            return Response(data={
                'data': serializer,
                'metadata': metadata
            },
                            status=200)
        except Exception as e:
            msg, code = e.args if len(e.args) == 2 else e.args, None
            return Response(data={
                'status': 'Failed!',
                'message': f'{msg}'
            },
                            status=code if code is not None else 400)

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            # serializer.save()
            return Response({"data": serializer.data}, 201)
        except Exception as e:
            msg, code = e.args if len(e.args) == 2 else e.args, None
            return Response(data={
                'status': 'Failed!',
                'message': f'{msg}'
            },
                            status=code if code is not None else 400)

    def retrieve(self, request, pk=None):
        try:
            queryset = models.UserProfile.objects.get(pk=pk)
            return Response(
                self.get_serializer(queryset, context={
                    'request': request
                }).data, 200)

        except (models.UserProfile.DoesNotExist, Exception) as e:
            msg, code = e.args if len(e.args) == 2 else e.args, None
            return Response(data={
                'status': 'Failed!',
                'message': f'{msg}'
            },
                            status=code if code is not None else 404)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            instance = models.UserProfile.objects.get(pk=pk)
            serializer = self.get_serializer(instance,
                                             data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            # serializer.save()
            return Response(data={
                'status': 'Thành công',
                'message': 'Cập nhật thành công',
                'data': serializer.data
            },
                            status=200)
        except (models.UserProfile.DoesNotExist, Exception) as e:
            msg, code = e.args if len(e.args) == 2 else e.args, None
            return Response(data={
                'status': 'Failed!',
                'message': f'{msg}'
            },
                            status=code if code is not None else 404)

    def destroy(self, request, pk=None):
        try:
            queryset = models.UserProfile.objects.get(pk=pk)
            # queryset.delete()
            self.perform_destroy(queryset)
            return Response({"message": "deleted", 'id': int(pk)}, 200)
        except (models.UserProfile.DoesNotExist, Exception) as e:
            msg, code = e.args if len(e.args) == 2 else e.args, None
            return Response(data={
                'status': 'Failed!',
                'message': f'{msg}'
            },
                            status=code if code is not None else 404)
