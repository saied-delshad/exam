from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from exam_sessions.api.serializers import SubjectSessionSerializer
from exam_sessions.models import SubjectExamSession, CourseExamSession



class SubjectSessionViewset(viewsets.ModelViewSet):
    queryset = SubjectExamSession.objects.all()
    lookup_field = "session_ref_number"
    serializer_class = SubjectSessionSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        
        if self.request.user.is_authenticated:
            session_queryset = SubjectExamSession.get_user_sessions(user=self.request.user)
        return session_queryset
