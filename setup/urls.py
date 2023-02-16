from django.urls import include, path, re_path
from rest_framework import routers
from users.views import UserView
from django.contrib import admin

from rest_framework import permissions


urlpatterns = [
    path('admin/', admin.site.urls),

    # urls about users
    path('users/', UserView.as_view()),
    path('users/<int:pk>', UserView.as_view()),    
]
