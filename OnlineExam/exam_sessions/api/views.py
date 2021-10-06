from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from exam_sessions.api.permissions import IsSubscribedInSession
from exam_sessions.api.serializers import SubjectSessionSerializer, ExamResultSerializer
from exam_sessions.models import SubjectExamSession, CourseExamSession, ExamResults



class SubjectSessionViewset(viewsets.ModelViewSet):
    queryset = SubjectExamSession.objects.all()
    lookup_field = "session_ref_number"
    serializer_class = SubjectSessionSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        
        if self.request.user.is_authenticated:
            session_queryset = SubjectExamSession.get_user_sessions(user=self.request.user)
        return session_queryset

class ExamResultCreateView(generics.CreateAPIView):
    queryset = ExamResults.objects.all()
    serializer_class = ExamResultSerializer
    permission_classes = [IsAuthenticated]


    def post(self, request, *args, **kwargs):
        print("22222222222222222")
        print(request.data)
        return super(ExamResultCreateView, self).post(request, *args, **kwargs)

    def perform_create(self, serializer):
        print("1111111111")
        print(self.kwargs)
        serializer.save(student = self.request.user)
