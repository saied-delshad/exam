from django.urls import include, path
from rest_framework.routers import DefaultRouter
from exam_sessions.api import views as sv

router = DefaultRouter()

router.register(r'sub-sessions', sv.SubjectSessionViewset)
router.register(r'cou-sessions', sv.CourseSessionViewset)
router.register(r'results', sv.ExamResultViewset)

urlpatterns = [
    path("", include(router.urls)),
]