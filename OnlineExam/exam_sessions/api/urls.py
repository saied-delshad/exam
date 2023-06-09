from django.urls import include, path
from rest_framework.routers import DefaultRouter
from exam_sessions.api import views as sv
from django.views.decorators.csrf import csrf_exempt

router = DefaultRouter()

router.register(r'sub-sessions', sv.SubjectSessionViewset)
router.register(r'cou-sessions', sv.CourseSessionViewset)
router.register(r'results', sv.ExamResultViewset),


urlpatterns = [
    path("", include(router.urls)),
    path("get-sessions/", csrf_exempt(sv.SessionRegister.as_view()), name="get_sessions"),
    path("list-sessions/", sv.SessionsViewset.as_view(), name="list_sessions"),
    path("list-sessions/<str:course>", sv.SessionsViewset.as_view(), name="list_course_sessions"),
    path("detail-result/<str:studentId>/<str:sessionRef>/", sv.ViewDetailResult.as_view(), name="detail_result")

]