from django.urls import include, path
from rest_framework.routers import DefaultRouter
from exam_sessions.api import views as sv

router = DefaultRouter()

router.register(r'sessions', sv.SubjectSessionViewset)
router.register(r'results', sv.ExamResultViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("updateresult/", sv.UpdateExamResult.as_view())
]