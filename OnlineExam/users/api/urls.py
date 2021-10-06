from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.api import views as uv

router = DefaultRouter()

router.register(r'users', uv.UserDisplayAPIViewset)

urlpatterns = [
    path("", include(router.urls))
]
