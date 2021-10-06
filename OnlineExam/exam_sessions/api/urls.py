from django.urls import include, path
from rest_framework.routers import DefaultRouter
from exam_sessions.api import views as sv

router = DefaultRouter()

router.register(r'sessions', sv.SubjectSessionViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("createresult/", sv.ExamResultCreateView.as_view())
]