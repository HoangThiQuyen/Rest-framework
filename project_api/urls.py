from django.urls import path, include
from project_api import views

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSets, basename='hello-viewset')
router.register('profile', views.UserProfileViewSet, basename='profile')

urlpatterns = [
    path('hello-apiview/', views.HelloAPIView.as_view()),
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
