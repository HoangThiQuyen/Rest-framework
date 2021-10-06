from django.contrib import admin
from django.urls import path, include, reverse
from drf_yasg import openapi
from django.conf.urls import url
from drf_yasg.views import get_schema_view
from rest_framework import permissions
import logging
from rest_framework.request import Request
from django.http import JsonResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s:%(levelname)s:%(module)s:%(lineno)d:%(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def get_current_host(self, request: Request) -> str:
    # TODO: Stup https for scheme
    scheme = request.scheme
    logger.info(f'{scheme}---{request.get_host()}')
    return f'https://{request.get_host()}'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('project_api.urls'))
]

schema_view = get_schema_view(
    openapi.Info(
        title="Quyen Demo",
        default_version='v1',
        description="Django Project Template Docs",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@hspace.biz"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser),
    permission_classes=(permissions.AllowAny, ),
)

# Docs urls
urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    url(r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-doc'),
    path('openapi',
         get_schema_view(title="Your Project",
                         description="API for all things …",
                         version="1.0.0"),
         name='openapi-schema'),
]
