from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views_api import HabitViewSet

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habit")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
