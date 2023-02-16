from django.urls import include, path, re_path
from rest_framework import routers
from users.views import UserView
from django.contrib import admin

from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # urls about users
    path('users/', UserView.as_view()),
    path('users/<int:pk>', UserView.as_view()),

    # Authenticated
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
