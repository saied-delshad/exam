from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from exam_sessions.api.permissions import IsSubscribedInSession, ExamResultOwner
from exam_sessions.api.serializers import SubjectSessionSerializer, ExamResultSerializer
from exam_sessions.models import SubjectExamSession, CourseExamSession, ExamResults


class SubjectSessionViewset(viewsets.ModelViewSet):
    queryset = SubjectExamSession.objects.all()
    lookup_field = "session_ref_number"
    serializer_class = SubjectSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            self.queryset = self.queryset.filter(participants__in=self.request.user.groups.all())
        return super(SubjectSessionViewset, self).get_queryset()


class ExamResultViewset(viewsets.ModelViewSet):
    queryset = ExamResults.objects.filter(is_finished=False)
    serializer_class = ExamResultSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "session_ref_number"

    def create(self, request, *args, **kwargs):
        request.data['student'] = request.user.id
        session_ref_number = request.data.get('session_ref_number')
        print(session_ref_number)
        return super(ExamResultViewset, self).create(request, *args, **kwargs)


class UpdateExamResult(generics.UpdateAPIView):
    queryset = ExamResults.objects.filter(is_finished=False)
    serializer_class = ExamResultSerializer
    permission_classes = [IsAuthenticated, ExamResultOwner]
    lookup_field = "session_ref_number"


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        return super(UpdateExamResult, self).update(request, *args, **kwargs)



