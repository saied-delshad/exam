from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from exam_sessions.api.permissions import IsSubscribedInSession, ExamResultOwner
from exam_sessions.api.serializers import SubjectSessionSerializer, CourseSessionSerializer, ExamResultSerializer, ExamResultWriteSerializer
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

    


class CourseSessionViewset(viewsets.ModelViewSet):
    queryset = CourseExamSession.objects.all()
    lookup_field = "session_ref_number"
    serializer_class = CourseSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        taken_exams = ExamResults.objects.filter(student = self.request.user)
        if self.request.user.is_authenticated:
            self.queryset = self.queryset.filter(participants__in=self.request.user.groups.all())
        if taken_exams:
            for item in taken_exams:
               self.queryset =  self.queryset.exclude(session_ref_number = item.session_ref_number)
        return super(CourseSessionViewset, self).get_queryset()


class ExamResultViewset(viewsets.ModelViewSet):
    queryset = ExamResults.objects.all()
    serializer_class = ExamResultSerializer
    permission_classes = [IsAuthenticated, ExamResultOwner]
    lookup_field = "session_ref_number"

    def get_queryset(self):
        self.queryset = self.queryset.filter(student=self.request.user)
        return super(ExamResultViewset, self).get_queryset()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            serializer_class = ExamResultSerializer
        else:
            serializer_class = ExamResultWriteSerializer
        return serializer_class

    def update(self, request, *args, **kwargs):
        print("888888888888888")
        print(kwargs)
        return super(ExamResultViewset, self).update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user, 
                        session_ref_number=self.request.data.get('session_ref_number'))





