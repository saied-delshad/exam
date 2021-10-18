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
        taken_exams = ExamResults.objects.filter(student = self.request.user)
        if self.request.user.is_authenticated:
            self.queryset = self.queryset.filter(participants__in=self.request.user.groups.all())
        if taken_exams:
            for item in taken_exams:
               self.queryset =  self.queryset.exclude(session_ref_number = item.session_ref_number)
        return super(SubjectSessionViewset, self).get_queryset()


class ExamResultViewset(viewsets.ModelViewSet):
    queryset = ExamResults.objects.filter(is_finished=False)
    serializer_class = ExamResultSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "session_ref_number"

    def get_queryset(self):
        self.queryset = self.queryset.filter(student=self.request.user)
        return super(ExamResultViewset, self).get_queryset()

    def create(self, request, *args, **kwargs):
        request.data['student'] = request.user.id
        session_ref_number = request.data.get('session_ref_number')
        return super(ExamResultViewset, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data['student'] = request.user.id
        request.data['session_ref_number'] = kwargs.get('session_ref_number', None)
        return super(ExamResultViewset, self).update(request, *args, **kwargs)





