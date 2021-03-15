from .views import UserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from django.urls import path, include

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]
